
from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract base model that provides created_at and updated_at.
    Other models can inherit these common fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ScootyColour(TimeStampedModel):
    colour_name = models.CharField(max_length=50, unique=True)
    colour_code = models.CharField(max_length=7, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "scooty_colour"
        ordering = ["colour_name"]
        verbose_name = "Scooty Colour"
        verbose_name_plural = "Scooty Colours"

    def __str__(self):
        return self.colour_name


class ScootyModel(TimeStampedModel):
    name = models.CharField(max_length=100)
    model_number = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    height = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )
    seat_length = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True
    )

    front_light = models.BooleanField(default=True)
    back_light = models.BooleanField(default=True)
    mirror = models.BooleanField(default=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "scooty_model"
        ordering = ["name"]
        verbose_name = "Scooty Model"
        verbose_name_plural = "Scooty Models"

    def __str__(self):
        return f"{self.name} ({self.model_number})"


class ScootyVariant(TimeStampedModel):
    scooty_model = models.ForeignKey(
        ScootyModel,
        on_delete=models.PROTECT,
        related_name="variants"
    )

    colour = models.ForeignKey(
        ScootyColour,
        on_delete=models.PROTECT,
        related_name="scooty_variants"
    )

    sku = models.CharField(max_length=50, unique=True)

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "scooty_variant"
        ordering = ["scooty_model__name", "colour__colour_name"]
        verbose_name = "Scooty Variant"
        verbose_name_plural = "Scooty Variants"

        constraints = [
            models.UniqueConstraint(
                fields=["scooty_model", "colour"],
                name="unique_scooty_model_colour"
            )
        ]

    def __str__(self):
        return f"{self.scooty_model.name} - {self.colour.colour_name}"


class ScootyUnit(TimeStampedModel):

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        RESERVED = "RESERVED", "Reserved"
        SOLD = "SOLD", "Sold"
        IN_REPAIR = "IN_REPAIR", "In Repair"
        DAMAGED = "DAMAGED", "Damaged"

    variant = models.ForeignKey(
        ScootyVariant,
        on_delete=models.PROTECT,
        related_name="units"
    )

    chassis_number = models.CharField(
        max_length=100,
        unique=True
    )

    motor_number = models.CharField(
        max_length=100,
        blank=True
    )

    purchase_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE
    )

    class Meta:
        db_table = "scooty_unit"
        ordering = ["-created_at"]
        verbose_name = "Scooty Unit"
        verbose_name_plural = "Scooty Units"

    def __str__(self):
        return f"{self.chassis_number} - {self.variant}"


class Battery(TimeStampedModel):

    class BatteryType(models.IntegerChoices):
        LITHIUM = 0, "Lithium"
        ION = 1, "Ion"

    class BMSType(models.IntegerChoices):
        JK_BMS = 0, "JK BMS"
        JP_BMS = 1, "JP BMS"

    name = models.CharField(max_length=100)

    battery_type = models.PositiveSmallIntegerField(
        choices=BatteryType.choices
    )

    bms_type = models.PositiveSmallIntegerField(
        choices=BMSType.choices
    )

    total_cell = models.PositiveIntegerField()

    charging_time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Charging time in hours"
    )

    run_time = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Expected running time in hours"
    )

    battery_lifecycle = models.PositiveSmallIntegerField(
        help_text="Expected battery lifespan in years"
    )

    app_control_supported = models.BooleanField(
        default=False,
        help_text="Whether Bluetooth mobile app control is supported"
    )

    voltage = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    capacity_ah = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        help_text="Battery capacity in Ampere-hours (Ah)"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Selling price for battery-only purchase"
    )

    scooty_bundle_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Battery price when purchased with a scooty"
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "battery"
        ordering = ["name"]
        verbose_name = "Battery"
        verbose_name_plural = "Batteries"

    def __str__(self):
        return self.name
