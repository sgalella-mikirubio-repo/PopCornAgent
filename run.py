from popcorn_agent import PopCornAgent


def main():
    # Set voice to true if you want to hear the agent. Set keyboard to false if
    # you prefer talking instead of typing.
    popcorn = PopCornAgent(voice=False, keyboard=True)
    popcorn.speak("Hi, I'm PopCorn. "
                  "What kind of film do you want to watch?")
    while not popcorn.end:
        user_message = popcorn.listen()  # TODO: If intelligible, ask again
        popcorn.parser(user_message)
        popcorn.name_managing()
        popcorn.consult_ontology()
        popcorn.response_generator()


if __name__ == "__main__":
    main()
