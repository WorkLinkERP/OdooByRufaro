#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script to verify the representative field implementation
"""

import os
import sys

def test_representative_field_in_model():
    """Test that the representative field is added to the account.move model"""
    print("🧪 Testing Representative Field in Account Move Model...")
    
    model_path = "models/account_move.py"
    if not os.path.exists(model_path):
        print("❌ Account move model file not found")
        return False
    
    with open(model_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "invoice_representative = fields.Char" not in content:
        print("❌ invoice_representative field not found in account move model")
        return False
    
    if "string='Representative'" not in content:
        print("❌ Representative field string not found")
        return False
    
    print("✅ invoice_representative field found in account move model")
    return True

def test_representative_field_in_view():
    """Test that the representative field is added to the invoice form view"""
    print("🧪 Testing Representative Field in Invoice Form View...")
    
    view_path = "views/account_move_views.xml"
    if not os.path.exists(view_path):
        print("❌ Account move views file not found")
        return False
    
    with open(view_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'name="invoice_representative"' not in content:
        print("❌ invoice_representative field not found in form view")
        return False
    
    if "Optional representative name for the invoice" not in content:
        print("❌ Representative field placeholder not found")
        return False
    
    print("✅ invoice_representative field found in form view")
    return True

def test_representative_field_in_template():
    """Test that the template uses the new representative field"""
    print("🧪 Testing Representative Field in Action Basin Template...")
    
    template_path = "report/invoice_template_action_basin.xml"
    if not os.path.exists(template_path):
        print("❌ Action Basin template file not found")
        return False
    
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 't-if="o.invoice_representative"' not in content:
        print("❌ Conditional display for representative field not found")
        return False
    
    if 't-field="o.invoice_representative"' not in content:
        print("❌ Representative field display not found in template")
        return False
    
    # Check that old user_id references are removed
    if 'o.invoice_user_id' in content or 'o.user_id.name' in content:
        print("❌ Old user_id references still present in template")
        return False
    
    print("✅ Representative field properly implemented in template")
    return True

def test_representative_field_conditional_display():
    """Test that the Rep section only shows when representative field is filled"""
    print("🧪 Testing Conditional Display Logic...")
    
    template_path = "report/invoice_template_action_basin.xml"
    with open(template_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Look for the specific pattern that shows Rep only when field is filled
    if '<div t-if="o.invoice_representative"><strong>Rep :</strong>' not in content:
        print("❌ Conditional display logic not properly implemented")
        return False
    
    print("✅ Conditional display logic properly implemented")
    return True

def main():
    """Run all tests"""
    print("🚀 Testing Representative Field Implementation\n")
    
    tests = [
        test_representative_field_in_model,
        test_representative_field_in_view,
        test_representative_field_in_template,
        test_representative_field_conditional_display,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()  # Add spacing between tests
        except Exception as e:
            print(f"❌ Test failed with error: {e}\n")
    
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Representative field implementation is complete.")
        print("\n📝 Summary of changes:")
        print("   • Added invoice_representative field to account.move model")
        print("   • Added representative field to invoice form view")
        print("   • Updated Action Basin template to use new field")
        print("   • Rep section only shows when representative field is filled")
        print("\n🔧 Next steps:")
        print("   • Restart Odoo server to load the new field")
        print("   • Update the module in Odoo")
        print("   • Test by creating an invoice and adding a representative name")
        return True
    else:
        print("❌ Some tests failed. Please review the implementation.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
