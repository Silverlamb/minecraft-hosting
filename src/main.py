from bot import DiscordClient

"""
Main function to start the central module
"""
def main():
    client = DiscordClient()
    client.run(client.token)


if __name__ == '__main__':
    main()
