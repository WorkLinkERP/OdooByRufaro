FROM odoo:19.0

USER root

# Copy your custom addons (create odoo_config/custom-addons if not exist)
COPY ./odoo_config/custom-addons /mnt/extra-addons

# Optional: copy your odoo.conf
# COPY ./odoo_config/conf/odoo.conf /etc/odoo/odoo.conf

# Fix permissions
RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069
