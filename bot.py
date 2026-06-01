import os
import logging

import discord


logger = logging.getLogger(__name__)


def get_required_int_env(name: str) -> int:
    value = os.getenv(name)
    if value is None:
        raise SystemExit(f"Missing required environment variable: {name}")
    try:
        return int(value)
    except ValueError as exc:
        raise SystemExit(f"{name} must be an integer") from exc


class DiscordMoverBot(discord.Client):
    def __init__(self, *, target_member_id: int, target_channel_id: int) -> None:
        intents = discord.Intents.default()
        intents.members = True
        intents.voice_states = True
        super().__init__(intents=intents)
        self.target_member_id = target_member_id
        self.target_channel_id = target_channel_id

    async def _move_if_needed(self, member: discord.Member) -> None:
        if member.voice is None or member.voice.channel is None:
            return

        target_channel = member.guild.get_channel(self.target_channel_id)
        if target_channel is None or not isinstance(
            target_channel, (discord.VoiceChannel, discord.StageChannel)
        ):
            logger.warning(
                "Target channel %s not found or not voice/stage in guild %s",
                self.target_channel_id,
                member.guild.id,
            )
            return

        if member.voice.channel.id == target_channel.id:
            return

        try:
            await member.move_to(
                target_channel,
                reason="Auto-moved by DiscordMoverBot to configured channel",
            )
        except (discord.Forbidden, discord.HTTPException) as exc:
            logger.warning("Failed to move target member: %s", exc)

    async def on_ready(self) -> None:
        for guild in self.guilds:
            member = guild.get_member(self.target_member_id)
            if member is not None:
                logger.info("Checking initial voice state for target member %s in guild %s", member.id, guild.id)
                await self._move_if_needed(member)

    async def on_voice_state_update(
        self,
        member: discord.Member,
        before: discord.VoiceState,
        after: discord.VoiceState,
    ) -> None:
        if member.id != self.target_member_id:
            return
        await self._move_if_needed(member)


def main() -> None:
    logging.basicConfig(level=logging.INFO)

    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise SystemExit("Missing required environment variable: DISCORD_TOKEN")

    bot = DiscordMoverBot(
        target_member_id=get_required_int_env("TARGET_MEMBER_ID"),
        target_channel_id=get_required_int_env("TARGET_CHANNEL_ID"),
    )
    bot.run(token)


if __name__ == "__main__":
    main()
