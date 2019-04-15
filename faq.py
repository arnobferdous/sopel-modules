from sopel.module import commands

answers = {
"": ""
}

@commands("faq")
def faq(bot, trigger):
    question = trigger.match.group(2)

    if question in answers:
        bot.say(answers[question])
