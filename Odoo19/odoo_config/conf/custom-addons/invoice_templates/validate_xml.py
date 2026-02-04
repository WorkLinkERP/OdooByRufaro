#!/usr/bin/env python3
"""
XML Validation Script for Invoice Templates Module

This script validates all XML files in the module to ensure they are well-formed
and can be parsed by Odoo without syntax errors.
"""

import os
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

def validate_xml_file(file_path):
    """Validate a single XML file"""
    try:
        ET.parse(file_path)
        return True, None
    except ET.ParseError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def find_xml_files():
    """Find all XML files in the module"""
    xml_files = []
    
    # Common directories that contain XML files
    xml_dirs = ['views', 'report', 'data', 'security', 'wizard']
    
    for xml_dir in xml_dirs:
        if os.path.exists(xml_dir):
            for root, dirs, files in os.walk(xml_dir):
                for file in files:
                    if file.endswith('.xml'):
                        xml_files.append(os.path.join(root, file))
    
    # Also check root directory for manifest and other XML files
    for file in os.listdir('.'):
        if file.endswith('.xml'):
            xml_files.append(file)
    
    return xml_files

def main():
    """Main validation function"""
    print("🔍 XML Validation for Invoice Templates Module\n")
    
    xml_files = find_xml_files()
    
    if not xml_files:
        print("❌ No XML files found in the module")
        return False
    
    print(f"Found {len(xml_files)} XML files to validate:\n")
    
    valid_count = 0
    invalid_files = []
    
    for xml_file in xml_files:
        print(f"Validating: {xml_file}")
        is_valid, error = validate_xml_file(xml_file)
        
        if is_valid:
            print(f"  ✅ Valid")
            valid_count += 1
        else:
            print(f"  ❌ Invalid: {error}")
            invalid_files.append((xml_file, error))
        
        print()
    
    print(f"📊 Validation Results:")
    print(f"  Valid files: {valid_count}/{len(xml_files)}")
    print(f"  Invalid files: {len(invalid_files)}")
    
    if invalid_files:
        print(f"\n❌ Invalid Files:")
        for file_path, error in invalid_files:
            print(f"  - {file_path}: {error}")
        print(f"\n💡 Common fixes:")
        print(f"  - Replace & with &amp; in XML attributes and text")
        print(f"  - Replace < with &lt; in text content")
        print(f"  - Replace > with &gt; in text content")
        print(f"  - Ensure all tags are properly closed")
        print(f"  - Check for unmatched quotes in attributes")
        return False
    else:
        print(f"\n🎉 All XML files are valid!")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
