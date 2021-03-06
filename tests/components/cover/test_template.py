"""The tests the cover command line platform."""

import logging
import unittest

from homeassistant.core import callback
from homeassistant import setup
import homeassistant.components.cover as cover
from homeassistant.const import STATE_OPEN, STATE_CLOSED

from tests.common import (
    get_test_home_assistant, assert_setup_component)
_LOGGER = logging.getLogger(__name__)


class TestTemplateCover(unittest.TestCase):
    """Test the cover command line platform."""

    hass = None
    calls = None
    # pylint: disable=invalid-name

    def setup_method(self, method):
        """Setup things to be run when tests are started."""
        self.hass = get_test_home_assistant()
        self.calls = []

        @callback
        def record_call(service):
            """Track function calls.."""
            self.calls.append(service)

        self.hass.services.register('test', 'automation', record_call)

    def teardown_method(self, method):
        """Stop everything that was started."""
        self.hass.stop()

    def test_template_state_text(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'value_template':
                                "{{ states.cover.test_state.state }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.set('cover.test_state', STATE_OPEN)
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_OPEN

        state = self.hass.states.set('cover.test_state', STATE_CLOSED)
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_CLOSED

    def test_template_state_boolean(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'value_template':
                                "{{ 1 == 1 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_OPEN

    def test_template_position(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ states.cover.test.attributes.position }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.set('cover.test', STATE_CLOSED)
        self.hass.block_till_done()

        entity = self.hass.states.get('cover.test')
        attrs = dict()
        attrs['position'] = 42
        self.hass.states.async_set(
            entity.entity_id, entity.state,
            attributes=attrs)
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('current_position') == 42.0
        assert state.state == STATE_OPEN

        state = self.hass.states.set('cover.test', STATE_OPEN)
        self.hass.block_till_done()
        entity = self.hass.states.get('cover.test')
        attrs['position'] = 0.0
        self.hass.states.async_set(
            entity.entity_id, entity.state,
            attributes=attrs)
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('current_position') == 0.0
        assert state.state == STATE_CLOSED

    def test_template_tilt(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'value_template':
                                "{{ 1 == 1 }}",
                            'tilt_template':
                                "{{ 42 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('current_tilt_position') == 42.0

    def test_template_out_of_bounds(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ -1 }}",
                            'tilt_template':
                                "{{ 110 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('current_tilt_position') is None
        assert state.attributes.get('current_position') is None

    def test_template_mutex(self):
        """Test that only value or position template can be used."""
        with assert_setup_component(0, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'value_template':
                                "{{ 1 == 1 }}",
                            'position_template':
                                "{{ 42 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'icon_template':
                                "{% if states.cover.test_state.state %}"
                                "mdi:check"
                                "{% endif %}"
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        assert self.hass.states.all() == []

    def test_template_position_or_value(self):
        """Test that at least one of value or position template is used."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'icon_template':
                                "{% if states.cover.test_state.state %}"
                                "mdi:check"
                                "{% endif %}"
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        assert self.hass.states.all() == []

    def test_template_non_numeric(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ on }}",
                            'tilt_template':
                                "{% if states.cover.test_state.state %}"
                                "on"
                                "{% else %}"
                                "off"
                                "{% endif %}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('current_tilt_position') is None
        assert state.attributes.get('current_position') is None

    def test_open_action(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 0 }}",
                            'open_cover': {
                                'service': 'test.automation',
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_CLOSED

        cover.open_cover(self.hass, 'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 1

    def test_close_stop_action(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 100 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'test.automation',
                            },
                            'stop_cover': {
                                'service': 'test.automation',
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_OPEN

        cover.close_cover(self.hass, 'cover.test_template_cover')
        self.hass.block_till_done()

        cover.stop_cover(self.hass, 'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 2

    def test_set_position(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 100 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.stop_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'set_cover_position': {
                                'service': 'test.automation',
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.state == STATE_OPEN

        cover.set_cover_position(self.hass, 42,
                                 'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 1

    def test_set_tilt_position(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 100 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.stop_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'set_cover_tilt_position': {
                                'service': 'test.automation',
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        cover.set_cover_tilt_position(self.hass, 42,
                                      'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 1

    def test_open_tilt_action(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 100 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.stop_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'set_cover_tilt_position': {
                                'service': 'test.automation',
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        cover.open_cover_tilt(self.hass, 'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 1

    def test_close_tilt_action(self):
        """Test the state text of a template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'position_template':
                                "{{ 100 }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.stop_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'set_cover_tilt_position': {
                                'service': 'test.automation',
                            },
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        cover.close_cover_tilt(self.hass, 'cover.test_template_cover')
        self.hass.block_till_done()

        assert len(self.calls) == 1

    def test_icon_template(self):
        """Test icon template."""
        with assert_setup_component(1, 'cover'):
            assert setup.setup_component(self.hass, 'cover', {
                'cover': {
                    'platform': 'template',
                    'covers': {
                        'test_template_cover': {
                            'value_template':
                                "{{ states.cover.test_state.state }}",
                            'open_cover': {
                                'service': 'cover.open_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'close_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'stop_cover': {
                                'service': 'cover.close_cover',
                                'entity_id': 'cover.test_state'
                            },
                            'icon_template':
                                "{% if states.cover.test_state.state %}"
                                "mdi:check"
                                "{% endif %}"
                        }
                    }
                }
            })

        self.hass.start()
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')
        assert state.attributes.get('icon') == ''

        state = self.hass.states.set('cover.test_state', STATE_OPEN)
        self.hass.block_till_done()

        state = self.hass.states.get('cover.test_template_cover')

        assert state.attributes['icon'] == 'mdi:check'
