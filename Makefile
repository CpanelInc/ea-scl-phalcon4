OBS_PROJECT := EA4-experimental
scl-php74-phalcon4-obs : DISABLE_BUILD += repository=CentOS_9 repository=Almalinux_10
scl-php73-phalcon4-obs : DISABLE_BUILD += repository=CentOS_9 repository=Almalinux_10
scl-php72-phalcon4-obs : DISABLE_BUILD += repository=CentOS_9 repository=Almalinux_10
include $(EATOOLS_BUILD_DIR)obs-scl.mk
