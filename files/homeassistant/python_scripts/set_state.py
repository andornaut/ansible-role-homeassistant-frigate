def set_state(entity_id, state, attributes, allow_create):
    """
    Set the state or other attributes of an entity

    Inspired by:
    https://github.com/xannor/hass_py_set_state/blob/master/python_scripts/set_state.py
    https://community.home-assistant.io/t/how-to-manually-set-state-value-of-sensor/43975/37
    """
    if not entity_id:
        logger.warning('An "entity_id" is required')
        return

    entity = hass.states.get(entity_id)
    if entity:
        old_attributes = entity.attributes.copy()
        old_attributes.update(attributes)
        attributes = old_attributes
        state = state or entity.state
    else:
        if not allow_create:
            logger.warning(
                'Cannot find an entity with id:%s. Set "allow_create" to allow an entity to be created',
                entity_id,
            )
            return
        if not state:
            logger.warning(
                'Cannot find an entity with id:%s and cannot create one either, because "state" is empty',
                entity_id,
            )
            return
        logger.debug(
            "Creating a new entity with id:%s, because one didn't exist and allow_create is True",
            entity_id,
        )

    logger.info(
        "Updating entity:%s with state:%s and attributes:%s",
        entity_id,
        state,
        attributes,
    )
    hass.states.set(entity_id, state, attributes)


EXCLUDED_KEYS = {"allow_create", "entity_id", "state"}
entity_id = data.get("entity_id")
state = data.get("state")
attributes = {k: v for k, v in data.items() if k not in EXCLUDED_KEYS}
allow_create = bool(data.get("allow_create"))
set_state(entity_id, state, attributes, allow_create)
