import re

def handler(event, context):
    """
    Entry-point for Serverless Function.
    :param event: request payload.
    :param context: information about current execution context.
    :return: response to be serialized as JSON.
    """
    answer = 'Я могу досчитать до целого числа от 1 до 100. До какого числа считать?'
    answer_tts = ''
    delay = 300 # Пауза в произношении.
    is_session_end = 'false'

    if event is not None and 'request' in event and 'original_utterance' in event['request'] and len(event['request']['original_utterance']):
        text = event['request']['command']
        num_susp = re.sub(r'\D', r'', text)
        if 'помощь' in text.lower() or 'что ты умеешь' in text.lower():
            answer = 'Я могу досчитать от одного до заданного числа. Число должно быть больше 1 и меньше 100. Вы называете это число, я считаю от одного до этого числа.'
        elif len(num_susp) and  0< int(num_susp) <=100:
            answer = ''
            delay_str = f' sil <[{delay}]> '
            for i in range(1, int(num_susp)+1):
                answer += str(i) + ' '
                answer_tts += str(i) + ' '
                if i%5 == 0:
                    answer_tts += delay_str
            answer += '. Закончила считать!'
            answer_tts += delay_str + 'Закончила считать!'
            answer = answer.replace(' .','.')
            is_session_end = 'true'
        else:
            answer = 'Пожалуйста, скажите число от 1 до 100'
    if not len(answer_tts):
        answer_tts = answer
    return {
        'version': event['version'],
        'session': event['session'],
        'response': {
            'text': answer,
            'tts': answer_tts,
            'end_session': is_session_end
        },
    }
