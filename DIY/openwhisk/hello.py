def main(args):
    first_name = args.get("first_name")
    last_name = args.get("last_name")
    message = 'Hello {} {}!'.format(first_name, last_name)
    return {"message": message}
