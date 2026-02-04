#!/usr/bin/env python3
"""
Test script to validate the Action Basin invoice template structure
and ensure it doesn't have unwanted header/footer elements.
"""

import xml.etree.ElementTree as ET
import sys
import os

def test_template_structure():
    """Test that the template structure is correct and self-contained."""
    
    # Test Action Basin template
    action_basin_path = "report/invoice_template_action_basin.xml"
    if not os.path.exists(action_basin_path):
        print(f"❌ Template file not found: {action_basin_path}")
        return False
    
    try:
        tree = ET.parse(action_basin_path)
        root = tree.getroot()
        
        # Check that we have the correct template structure
        template = root.find(".//template[@id='report_invoice_action_basin']")
        if template is None:
            print("❌ Action Basin template not found")
            return False
        
        # Check that we're using web.html_container (good)
        html_container = template.find(".//t[@t-call='web.html_container']")
        if html_container is None:
            print("❌ web.html_container not found")
            return False
        
        # Check that we're NOT using web.external_layout (good - this was the problem)
        external_layout = template.find(".//t[@t-call='web.external_layout']")
        if external_layout is not None:
            print("❌ Still using web.external_layout - this will cause header/footer issues")
            return False
        
        # Check that we have the basic div structure
        article_div = template.find(".//div[@class='article o_report_layout_standard']")
        if article_div is None:
            print("❌ Article div with correct class not found")
            return False
        
        # Check that we have embedded CSS for styling control
        style_tag = template.find(".//style")
        if style_tag is None:
            print("❌ Embedded style tag not found")
            return False
        
        print("✅ Action Basin template structure is correct")
        print("✅ Not using web.external_layout (avoids default headers/footers)")
        print("✅ Using web.html_container (provides basic HTML structure)")
        print("✅ Has embedded CSS for complete styling control")
        
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error in Action Basin template: {e}")
        return False

def test_modern_template():
    """Test that the Modern template is also correctly structured."""
    
    modern_path = "report/invoice_template_modern.xml"
    if not os.path.exists(modern_path):
        print(f"❌ Template file not found: {modern_path}")
        return False
    
    try:
        tree = ET.parse(modern_path)
        root = tree.getroot()
        
        # Check that we have the correct template structure
        template = root.find(".//template[@id='report_invoice_modern']")
        if template is None:
            print("❌ Modern template not found")
            return False
        
        # Check that we're NOT using web.external_layout
        external_layout = template.find(".//t[@t-call='web.external_layout']")
        if external_layout is not None:
            print("❌ Modern template still using web.external_layout")
            return False
        
        print("✅ Modern template structure is also correct")
        return True
        
    except ET.ParseError as e:
        print(f"❌ XML parsing error in Modern template: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing invoice template structure...")
    print("=" * 50)
    
    success = True
    success &= test_template_structure()
    success &= test_modern_template()
    
    print("=" * 50)
    if success:
        print("🎉 All tests passed! Templates should now work without unwanted headers/footers.")
        print("\n📋 What was fixed:")
        print("   • Removed web.external_layout dependency")
        print("   • Added CSS reset to remove list styling (black dots)")
        print("   • Disabled default Odoo headers and footers")
        print("   • Made templates completely self-contained")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the template structure.")
        sys.exit(1)
