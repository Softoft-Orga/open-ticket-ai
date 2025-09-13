from open_ticket_ai.src.core.config.config_models import load_config


def test_load_yaml_config():
    config = load_config('./config.yml')
    print(config)
