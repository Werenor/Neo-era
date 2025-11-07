from neoera import renderer_gui as renderer
from neoera.runtime import Context
ctx = Context()
ctx.set("player_name", "指挥官")

if __name__ == "__main__":
    renderer.load_background("assets/bg/test_bg.jpg")
    renderer.echo("[Neo-era] 引擎初始化完成。")
    renderer.echo("爱宕：早安，指挥官。")

    idx = renderer.print_choice(["回应", "装作没听见"])
    if idx == 0:
        renderer.echo("玩家：早安，爱宕。")
        renderer.echo("爱宕：真贴心呢~")
    else:
        renderer.echo("爱宕：哼。")

    renderer.wait_for_key()
