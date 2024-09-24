"""Admin site."""

from django.contrib import admin

from metenox.models import (
    EveTypePrice,
    HoldingCorporation,
    Metenox,
    MetenoxHourlyProducts,
    MetenoxStoredMoonMaterials,
    Moon,
    Owner,
)
from metenox.templatetags.metenox import formatisk


class MetenoxHourlyHarvestInline(admin.TabularInline):
    model = MetenoxHourlyProducts

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Moon)
class MoonAdmin(admin.ModelAdmin):
    list_display = ["name", "moon_value", "value_updated_at"]
    fields = [("eve_moon", "moonmining_moon"), ("value", "value_updated_at")]
    search_fields = ["eve_moon__name"]
    readonly_fields = ["eve_moon", "moonmining_moon"]
    inlines = (MetenoxHourlyHarvestInline,)

    @admin.display(description="value")
    def moon_value(self, moon: Moon):
        return f"{formatisk(moon.value)} ISK"

    def has_add_permission(self, request):
        return False


class MetenoxMoonMaterialBayInline(admin.TabularInline):
    model = MetenoxStoredMoonMaterials

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Metenox)
class MetenoxAdmin(admin.ModelAdmin):
    list_display = [
        "structure_name",
        "corporation",
        "alliance",
        "metenox_value",
        "fuel_blocks_count",
        "magmatic_gas_count",
    ]
    list_filter = ["corporation", "corporation__corporation__alliance"]
    fields = [
        ("structure_id", "structure_name"),
        "moon",
        "corporation",
        ("fuel_blocks_count", "magmatic_gas_count"),
    ]
    readonly_fields = ["structure_id", "moon"]
    inlines = (MetenoxMoonMaterialBayInline,)

    @admin.display(description="Value", ordering="moon__value")
    def metenox_value(self, metenox: Metenox):
        return f"{formatisk(metenox.moon.value)} ISK"

    @admin.display(
        description="Corporation alliance",
        ordering="corporation__corporation__alliance",
    )
    def alliance(self, metenox: Metenox):
        return metenox.corporation.alliance

    def has_add_permission(self, request):
        return False


@admin.action(description="Enable selected owners")
def enable_owners(modeladmin, request, queryset):
    """Enable all owners of the received queryset"""
    Owner.enable_owners(queryset)


@admin.action(description="Disable selected owners")
def disable_owners(modeladmin, request, queryset):
    """Disable all owners of the received queryset"""
    Owner.disable_owners(queryset)


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = [
        "char_name",
        "is_enabled",
        "corporation",
        "ally_name",
        "character_ownership",
    ]
    list_filter = ["is_enabled", "corporation", "corporation__corporation__alliance"]
    readonly_fields = ["character_ownership", "corporation"]
    actions = [enable_owners, disable_owners]

    @admin.display(
        description="Character name", ordering="character_ownership__character"
    )
    def char_name(self, owner: Owner) -> str:
        return owner.character_name

    @admin.display(
        description="Alliance name", ordering="corporation__corporation__alliance"
    )
    def ally_name(self, owner: Owner) -> str:
        return owner.alliance_name

    def has_add_permission(self, request):
        return False


@admin.action(description="Enable all owners of the corporations")
def enable_all_owners(modeladmin, request, queryset):
    """Enable all owners part of the corporations listed"""
    HoldingCorporation.enable_all_owners(queryset)


@admin.action(description="Disable all owners of the corporations")
def disable_all_owners(modeladmin, request, queryset):
    """Disable all owners part of the corporations listed"""
    HoldingCorporation.disable_all_owners(queryset)


class OwnerCharacterAdminInline(admin.TabularInline):
    model = Owner
    readonly_fields = ["character_ownership"]

    fields = ["character_ownership", "is_enabled"]

    def has_add_permission(self, request, obj):
        return False


@admin.register(HoldingCorporation)
class HoldingCorporationAdmin(admin.ModelAdmin):
    list_display = [
        "corporation",
        "alliance",
        "is_active",
        "count_metenox",
        "count_owners",
        "last_updated",
    ]
    list_filter = ["corporation__alliance", "is_active"]
    sortable_by = ["is_active"]
    actions = [enable_all_owners, disable_all_owners]
    readonly_fields = ["corporation", "last_updated", "count_metenox"]
    inlines = (OwnerCharacterAdminInline,)

    @admin.display(description="Number metenoxes")
    def count_metenox(self, holding: HoldingCorporation) -> int:
        return holding.count_metenoxes

    @admin.display(
        description="Number of owners / active owners", ordering="owners__count"
    )
    def count_owners(self, holding: HoldingCorporation) -> str:
        return f"{holding.owners.count()} / {holding.active_owners().count()}"

    def has_add_permission(self, request):
        return False


@admin.register(EveTypePrice)
class EveTypePriceAdmin(admin.ModelAdmin):
    list_display = ["eve_type", "eve_group", "type_price"]
    readonly_fields = ["eve_type", "last_update"]

    @admin.display(description="Price", ordering="price")
    def type_price(self, type_price: EveTypePrice):
        return f"{formatisk(type_price.price)} ISK"

    @admin.display(description="Eve Group", ordering="eve_type__eve_group")
    def eve_group(self, type_price: EveTypePrice):
        return type_price.eve_type.eve_group

    def has_add_permission(self, request):
        return False
