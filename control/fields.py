from django.db import models


class EnumCharField(models.CharField):
    def db_type(self, connection):
        if connection.vendor != "mysql":
            return super().db_type(connection)

        values = []
        for choice in self.choices:
            value = choice[0]
            escaped = str(value).replace("\\", "\\\\").replace("'", "\\'")
            values.append(f"'{escaped}'")
        return f"enum({', '.join(values)})"
