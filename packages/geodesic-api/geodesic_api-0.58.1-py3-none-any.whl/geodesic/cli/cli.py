import json
import geodesic
import geodesic.config as config
import argparse


def authenticate_command(args):
    geodesic.authenticate(port_override=args.port, name=args.name, host=args.host)


def get_command(args):
    cm = config.ConfigManager()

    if args.resource == "clusters":
        clusters, active = cm.list_configs()
        for cluster in clusters:
            if cluster == active:
                print(f"[*] {cluster}")
            else:
                print(f"[ ] {cluster}")
    elif args.resource == "active-config":
        cfg = cm.get_active_config()
        print(json.dumps(cfg.to_dict(), indent=4, sort_keys=True))


def set_command(args):
    cm = config.ConfigManager()

    if args.resource == "cluster":
        active = args.value
        cm.set_active_config(active)


def validate_command(args):
    import geodesic.tesseract.models.validate as validate

    validator = validate.ValidationManager(image=args.image, cli=True)
    validator.run()


def make_parser():
    parser = argparse.ArgumentParser(prog="geodesic")
    parser.set_defaults(func=lambda args: parser.print_help())

    subparsers = parser.add_subparsers(
        title="subcommand", description="valid subcommands", help="which action to run"
    )

    # Authentication Parser stuff
    parser_authenticate = subparsers.add_parser(
        "authenticate", help="authenticate your account for use with this API"
    )
    parser_authenticate.add_argument(
        "-p",
        "--port",
        required=False,
        type=int,
        help="a port on your machine which can be used to run the code fetching server, "
        "removing the need to manually copy-paste auth code. "
        "If not specified, defaults to 8080. "
        "Please note that not all ports may be enabled in your OAuth provider's list "
        "of allowed callback URLs. This is only used for direct oauth2 authentication (uncommon).",
    )
    parser_authenticate.add_argument(
        "-n",
        "--name",
        required=False,
        type=str,
        help="the name of the cluster to authenticate against",
    )
    parser_authenticate.add_argument(
        "-H",
        "--host",
        required=False,
        type=str,
        help="the host of the cluster to authenticate against"
        " (e.g. https://api.geodesic.seerai.space)",
    )
    parser_authenticate.set_defaults(func=authenticate_command)

    # Cluster config parser stuff
    parser_get = subparsers.add_parser("get", help="get resource")
    parser_get.add_argument(
        "resource",
        choices=["clusters", "active-config"],
        help="get specified resource. Output depends on the requested resource",
    )
    parser_get.set_defaults(func=get_command)

    parser_set = subparsers.add_parser("set", help="set resource")
    parser_set.add_argument("resource", choices=["cluster"], type=str, help="resources to set")
    parser_set.add_argument("value", type=str, help="resource value to set (e.g. cluster name)")
    parser_set.set_defaults(func=set_command)

    # Tesseract Model image testing
    parser_model_validation = subparsers.add_parser(
        "validate", help="validate your model container for use in Tesseract jobs"
    )
    parser_model_validation.add_argument(
        "image",
        type=str,
        help="the image and tag to validate, e.g. my-model-container:v0.0.1",
    )
    parser_model_validation.set_defaults(func=validate_command)

    return parser


def main():
    args = make_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
