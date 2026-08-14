import xmlschema

def main():
    xsd_path = 'vehicles.xsd'
    xml_path = 'vehicles.xml'

    print("Loading schema...")
    # Load the XSD schema
    schema = xmlschema.XMLSchema(xsd_path)
    
    print("Validating XML...")
    # Validate the XML file
    if schema.is_valid(xml_path):
        print("Success: The XML document is valid according to the schema!")
    else:
        print("Error: The XML document is invalid.")

if __name__ == '__main__':
    main()
