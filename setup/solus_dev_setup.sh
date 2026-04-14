#!/bin/bash
clear

mkdir -p "$HOME/.config/solus"

PKGR_NAME=""
PKGR_EMAIL=""
PKGR_MATRIX=""


echo "------------------------------"
echo " Setup Packager File"
echo "------------------------------"

# Prompt the user for their details
read -p "Enter your Name: " PKGR_NAME
read -p "Enter your Email: " PKGR_EMAIL
read -p "Enter your Matrix Username: " PKGR_MATRIX

# Write the inputs to the packager file
echo "[Packager]" > "$HOME/.config/solus/packager"
echo "Name=${PKGR_NAME}" >> "$HOME/.config/solus/packager"
echo "Email=${PKGR_EMAIL}" >> "$HOME/.config/solus/packager"
echo "Matrix=${PKGR_MATRIX}" >> "$HOME/.config/solus/packager"

echo "Packager file  created at $HOME/.config/solus/packager"


echo "------------------------------"
echo " Packager File Content"
echo "------------------------------"
cat "$HOME/.config/solus/packager"


echo -e "\n------------------------------"
echo " Install Dev Tools"
echo "------------------------------"

sudo eopkg it --reinstall ent git github-cli golang  go-task intltool jq solbuild solbuild-config-unstable ypkg yq micro nextcloud-client featherpad fish solseek font-firacode-nerd adwaita-fonts
sudo eopkg remove libreoffice-common thunderbird thunderbird-langpacks -y
flatpak install flathub it.mijorus.gearlever -y

echo -e "\n------------------------------"
echo " Set Fish as default shell"
echo "------------------------------"

chsh -s /usr/bin/fish


echo -e "\n------------------------------"
echo "Setting up solbuild"
echo "------------------------------"
sudo solbuild init
sudo solbuild update

echo -e "\n------------------------------"
echo " Configure github-cli"
echo "------------------------------"

git config --global user.name "${PKGR_NAME}"
git config --global user.email "${PKGR_EMAIL}"

gh auth login


cd 
gh repo clone packages ~/solus-packages

go-task -d ~/solus-packages init

echo -e "\n------------------------------"
echo " Setup helper functions"
echo "------------------------------"

mkdir -p ~/.bashrc.d
chmod 700 ~/.bashrc.d
ln -s ~/solus-packages/common/Scripts/helpers.sh ~/.bashrc.d/solus-monorepo-helpers.sh
source ~/.bashrc

mkdir -p ~/.config/fish/conf.d
ln -s ~/solus-packages/common/Scripts/helpers.fish ~/.config/fish/conf.d/solus.fish


echo -e "\n------------------------------"
echo " Finished W"
echo "------------------------------"
