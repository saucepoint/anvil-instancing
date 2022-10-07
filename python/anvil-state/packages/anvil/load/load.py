def main(args):
      name = args.get("name", "LOAD")
      greeting = "Hello " + name + "!"
      print(greeting)
      return {"body": greeting}
  