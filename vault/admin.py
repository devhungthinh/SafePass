from django.contrib import admin


from vault.models import (
  Vault, 
  PasswordEntry,
  PasswordHistory,
  Website,
)


class WebsiteInline(admin.TabularInline):
  model = Website
  extra = 1


class PasswordHistoryInline(admin.TabularInline):
  model = PasswordHistory
  extra=1


@admin.register(PasswordEntry)
class PasswordEntryAdmin(admin.ModelAdmin):
  inlines = [PasswordHistoryInline, WebsiteInline]


@admin.register(PasswordHistory)
class PasswordHistoryAdmin(admin.ModelAdmin):
  list_display = [field.name for field in PasswordHistory._meta.fields]


@admin.register(Vault)
class VaultAdmin(admin.ModelAdmin):
  pass


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
  pass
