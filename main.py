import interactions
from . import pet_dataset

pet_manager = pet_dataset.PetManager()


async def my_id(ctx: interactions.BaseContext):
    if str(ctx.user.id) == '1029957776841130075': return True
    return False


class Base(interactions.Extension):
    module_base: interactions.SlashCommand = interactions.SlashCommand(
        name="pet",
        description="获得一只宠物。喂食，抚摸，或者安排它工作。"
    )

    # 管理员指令：添加指定数量的物品给某人。
    @module_base.subcommand("send", sub_cmd_description="送给某人一只宠。")
    @interactions.check(my_id)
    @interactions.slash_option(
        name="user_id",
        description="接收人",
        required=True,
        opt_type=interactions.OptionType.USER
    )
    @interactions.slash_option(
        name="name",
        description="宠物名",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    @interactions.slash_option(
        name="img_path",
        description="宠物头像",
        required=True,
        opt_type=interactions.OptionType.STRING
    )
    async def command_get_item(self, ctx: interactions.SlashContext, user_id: str, name: str,
                               img_path: str):
        user_id = str(user_id)
        pet_manager.add_pet(user_id, name, img_path)
        await ctx.send(f"<@{user_id}>获得一只宠物！")
