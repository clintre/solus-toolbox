import xmltodict

# Sample XML string
xml_data = """<?xml version="1.0"?>
<library>
    <book id="1">
        <title>Testing Solus Packages</title>
        <author>Package Maintainer</author>
    </book>
</library>
"""

def main():
    # Test parse() - XML to Dictionary
    data_dict = xmltodict.parse(xml_data)
    print("Parsed XML into Dictionary successfully:")
    title = data_dict['library']['book']['title']
    print(f" - Book Title: {title}")

    # Test unparse() - Dictionary back to XML
    regenerated_xml = xmltodict.unparse(data_dict, pretty=True)
    print("\nRegenerated XML from Dictionary:")
    print(regenerated_xml)

if __name__ == '__main__':
    main()
