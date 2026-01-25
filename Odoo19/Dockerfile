FROM odoo:19.0

USER root

COPY ./odoo_config/custom-addons /mnt/extra-addons

# Optional: copy odoo.conf
# COPY ./odoo_config/conf/odoo.conf /etc/odoo/odoo.conf

RUN chown -R odoo:odoo /mnt/extra-addons

USER odoo

EXPOSE 8069
