# DiscordMoverBot
A discord bot that automatically moves a member to a voice channel.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set environment variables:
   - `DISCORD_TOKEN`: Bot token
   - `TARGET_MEMBER_ID`: Discord user ID to move
   - `TARGET_CHANNEL_ID`: Voice channel ID to move the user into
3. Run the bot:
   ```bash
   python bot.py
   ```

## Discord permissions/intents

- Enable the **Server Members Intent** for the bot in the Discord Developer Portal.
- Ensure the bot has permission to **View Channels**, **Connect**, and **Move Members** in the target server.
