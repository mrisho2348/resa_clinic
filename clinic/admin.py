from django.contrib import admin

from clinic.models import BankAccount, Client, DeductionOrganization, Employee, EmployeeDeduction, Expense, ExpenseCategory, Invoice, Payment, PaymentMethod, Payroll, SalaryChangeRecord, SalaryPayment

# Register your models here.
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'employee_id', 'department', 'employment_type', 'start_date', 'end_date', 'salary')
    search_fields = ['name__name', 'employee_id', 'department']
    list_filter = ('department', 'employment_type', 'start_date', 'end_date')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name',  'department', 'employment_type', 'start_date', 'end_date')
        }),
        ('Salary and Bank Details', {
            'fields': ('salary', 'bank_account', 'bank_account_number', 'account_holder_name')
        }),
        ('Organization-specific Identification Numbers', {
            'fields': ('tin_number', 'nssf_membership_number', 'nhif_number', 'wcf_number')
        }),
        ('Deduction Status', {
            'fields': ('tra_deduction_status', 'nssf_deduction_status', 'wcf_deduction_status', 'heslb_deduction_status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset by default
        }),
    )

admin.site.register(Employee, EmployeeAdmin)


class DeductionOrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'rate', 'created_at', 'updated_at')
    search_fields = ['name']
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Organization Information', {
            'fields': ('name', 'rate', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(DeductionOrganization, DeductionOrganizationAdmin)


class EmployeeDeductionAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll', 'organization', 'deducted_amount', 'created_at', 'updated_at')
    search_fields = ['employee__name', 'payroll__payroll_date', 'organization__name']
    list_filter = ('created_at', 'updated_at', 'organization')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Deduction Information', {
            'fields': ('employee', 'payroll', 'organization', 'deducted_amount')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

    def has_add_permission(self, request):
        return False  # Disable adding permission

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing permission


admin.site.register(EmployeeDeduction, EmployeeDeductionAdmin)

class SalaryChangeRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll', 'previous_salary', 'new_salary', 'change_date', 'created_at', 'updated_at')
    search_fields = ['employee__name', 'payroll__payroll_date']
    list_filter = ('change_date', 'created_at', 'updated_at')
    readonly_fields = ('change_date', 'created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Salary Change Information', {
            'fields': ('employee', 'payroll', 'previous_salary', 'new_salary', 'change_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )
    def has_add_permission(self, request):
        return False  # Disable adding permission

    def has_change_permission(self, request, obj=None):
        return False  # Disable editing permission
admin.site.register(SalaryChangeRecord, SalaryChangeRecordAdmin)

class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Payment Method Information', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(PaymentMethod, PaymentMethodAdmin)

class ExpenseCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at', 'updated_at')
    search_fields = ['name']
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Expense Category Information', {
            'fields': ('name', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(ExpenseCategory, ExpenseCategoryAdmin)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'description', 'category', 'created_at', 'updated_at')
    search_fields = ['date', 'amount', 'description', 'category__name']
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Expense Information', {
            'fields': (('date', 'amount'), 'description', 'category', 'additional_details', 'receipt')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(Expense, ExpenseAdmin)

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('number', 'date', 'due_date', 'amount', 'status', 'client', 'created_at', 'updated_at')
    search_fields = ['number', 'date', 'due_date', 'amount', 'status', 'client__name']
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Invoice Information', {
            'fields': (('number', 'status'), ('date', 'due_date'), 'amount', 'client')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(Invoice, InvoiceAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'method', 'invoice', 'created_at', 'updated_at')
    search_fields = ['date', 'amount', 'description']
    list_filter = ('date', 'method', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Payment Information', {
            'fields': (('date', 'amount'), 'method', 'invoice', 'description')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(Payment, PaymentAdmin)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone_number', 'address', 'contact_person', 'created_at', 'updated_at')
    search_fields = ['name', 'email', 'phone_number', 'contact_person']
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Client Information', {
            'fields': ('name', 'email', 'phone_number', 'address', 'contact_person')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(Client, ClientAdmin)


class PayrollAdmin(admin.ModelAdmin):
    list_display = ('payroll_date', 'total_salary', 'status', 'payment_method', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Payroll Information', {
            'fields': ('payroll_date', 'total_salary', 'status', 'payment_method', 'details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(Payroll, PayrollAdmin)

class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Bank Account Information', {
            'fields': ('bank_name',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(BankAccount, BankAccountAdmin)


class SalaryPaymentAdmin(admin.ModelAdmin):
    list_display = ('employee', 'payroll','payment_date', 'payment_status')
    readonly_fields = ('created_at', 'updated_at')  # Optionally, make certain fields read-only

    fieldsets = (
        ('Payment Information', {
            'fields': ('employee', 'payroll',  'payment_date', 'payment_status', 'payment_details')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Optionally, collapse this fieldset
        }),
    )

admin.site.register(SalaryPayment, SalaryPaymentAdmin)