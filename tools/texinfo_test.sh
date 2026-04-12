#!/bin/bash
clear
# texinfo Regression & Timing Test Script for Solus Linux

# Ensure required utilities are installed
for cmd in awk zstd unzstd; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "Error: '$cmd' is required but not installed."
        exit 1
    fi
done

if ! command -v makeinfo &> /dev/null; then
    echo "Error: 'texinfo' package is not installed."
    exit 1
fi

echo -e "\033[1m============================================================\033[0m"
echo " Starting texinfo Regression Tests v0.2"
echo " Texinfo version: $(makeinfo --version | head -n 1)"
echo -e "\033[1m============================================================\033[0m"

# Setup isolated testing directory
WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT
cd "$WORKDIR" || exit 1


# Test Helper Function (Runs command, times it, and checks success)

run_test() {
    local test_name="$1"
    shift
    local cmd=("$@")

    printf "Testing %-35s " "$test_name..."

    local start_time=$(date +%s%3N)
    "${cmd[@]}" > "${test_name// /_}.log" 2>&1
    local exit_code=$?
    local end_time=$(date +%s%3N)

    local elapsed_ms=$((end_time - start_time))
    local elapsed_sec=$(awk -v ms="$elapsed_ms" 'BEGIN {printf "%.3f", ms/1000}')

    if [ $exit_code -eq 0 ]; then
        echo -e "[\033[32mPASS\033[0m] (${elapsed_sec}s)"
    else
        echo -e "[\033[31mFAIL\033[0m] (${elapsed_sec}s)"
        echo "    -> LOG OUTPUT:"
        sed 's/^/       /' "${test_name// /_}.log"
    fi
    return $exit_code
}


# Generate Dummy Test Files

cat << 'EOF' > sample.texi
\input texinfo
@setfilename sample.info
@settitle Sample Manual

@dircategory Regression Testing
@direntry
* Sample Manual: (sample).  The sample manual used for testing.
@end direntry

@node Top
@top Sample Manual

Welcome to the Sample Manual used for regression testing.
@bye
EOF

cat << 'EOF' > sample.pod
=head1 NAME
sample - A sample pod file for testing
=head1 SYNOPSIS
This is used to test pod2texi.
EOF


# Test Core Functions & Converters

run_test "makeinfo (Info generation)" makeinfo sample.texi
run_test "makeinfo (HTML generation)" makeinfo --html sample.texi
run_test "makeinfo (Plaintext generation)" makeinfo --plaintext -o sample.txt sample.texi
run_test "makeinfo (DocBook generation)" makeinfo --docbook -o sample.xml sample.texi
run_test "makeinfo (Texinfo XML generation)" makeinfo --xml sample.texi
run_test "pod2texi (Perl POD conversion)" pod2texi sample.pod


# Test Utilities (Standard)
touch dir
printf "Testing %-35s " "install-info (Directory update)..."
start_time=$(date +%s%3N)
install-info sample.info dir > install_info_std.log 2>&1
exit_code=$?
end_time=$(date +%s%3N)
elapsed_ms=$((end_time - start_time))
elapsed_sec=$(awk -v ms="$elapsed_ms" 'BEGIN {printf "%.3f", ms/1000}')

if [ $exit_code -eq 0 ] && grep -q "Sample Manual" dir; then
     echo -e "[\033[32mPASS\033[0m] (${elapsed_sec}s)"
else
     echo -e "[\033[31mFAIL\033[0m] (${elapsed_sec}s)"
     echo "    -> LOG OUTPUT:"
     sed 's/^/       /' install_info_std.log
fi

run_test "info (Read standard .info file)" info --file ./sample.info --subnodes -o standard_info_dump.txt


# Test zstd Compression Support (Fedora-like patch)
echo -e "\033[1m------------------------------------------------------------\033[0m"
echo " Testing zstd Compression Support"

echo " - Note:
   Unpatched will FAIL the Magic byte detect but PASS unzstd.
   Patch Should PASS both."
echo -e "\033[1m------------------------------------------------------------\033[0m"

# Step 1: Create a totally unique file specifically for the zstd test
cat << 'EOF' > solus_zstd_test.texi
\input texinfo
@setfilename zstd_test.info
@settitle ZSTD Test Manual

@dircategory Regression Testing
@direntry
* ZSTD Test: (solus_zstd_test).  ZSTD test entry.
@end direntry

@node Top
@top ZSTD Test Manual

SOLUS_ZSTD_MAGIC_STRING_777
@bye
EOF

# Step 2: Compile it to standard info format
makeinfo solus_zstd_test.texi

# Step 3: Compress it with zstd and definitively delete the uncompressed originals
zstd -q --rm zstd_test.info
rm -f solus_zstd_test.texi zstd_test.info

if [ -f "zstd_test.info.zst" ]; then

    # Isolate it in a new folder to block path traversal
    mkdir zstd_isolate
    mv zstd_test.info.zst zstd_isolate/
    cd zstd_isolate || exit 1

    # Test A: install-info magic byte detection


    printf "Testing %-35s " "install-info (Magic byte detect)..."
    start_time=$(date +%s%3N)

    touch dir
    install-info zstd_test.info.zst dir > install_info_zst.log 2>&1
    exit_code=$?

    end_time=$(date +%s%3N)
    elapsed_ms=$((end_time - start_time))
    elapsed_sec=$(awk -v ms="$elapsed_ms" 'BEGIN {printf "%.3f", ms/1000}')

    if [ $exit_code -eq 0 ] && grep -q "ZSTD Test" dir; then
         echo -e "[\033[32mPASS\033[0m] (${elapsed_sec}s)"
    else
         echo -e "[\033[31mFAIL\033[0m] (${elapsed_sec}s)"
         echo "    -> LOG OUTPUT:"
         sed 's/^/       /' install_info_zst.log
    fi

    # Test B: info reader filesys fallback
    printf "Testing %-35s " "info (Auto-resolve via unzstd)..."
    start_time=$(date +%s%3N)

    # Execute info reader
    info --file ./zstd_test.info --subnodes -o zstd_info_dump.txt > zstd_read.log 2>&1
    exit_code=$?

    end_time=$(date +%s%3N)
    elapsed_ms=$((end_time - start_time))
    elapsed_sec=$(awk -v ms="$elapsed_ms" 'BEGIN {printf "%.3f", ms/1000}')

    # Did it successfully extract the magic string?
    if [ $exit_code -eq 0 ] && grep -q "SOLUS_ZSTD_MAGIC_STRING_777" zstd_info_dump.txt 2>/dev/null; then
         echo -e "[\033[32mPASS\033[0m] (${elapsed_sec}s)"
         echo "    -> SUCCESS! Piped the zst archive through unzstd."
    else
         echo -e "[\033[31mFAIL\033[0m] (${elapsed_sec}s)"
         echo "    -> 'info' failed to decompress the .zst file."
         echo "    -> LOG OUTPUT:"
         sed 's/^/       /' zstd_read.log
    fi

    cd ..
else
    echo -e "Testing zstd compression creation... [\033[31mFAIL\033[0m]"
fi

echo -e "\033[1m============================================================\033[0m"
echo " Tests completed. Temporary files will be cleaned up."
echo -e "\033[1m============================================================\033[0m"
