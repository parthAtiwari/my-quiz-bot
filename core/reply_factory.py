
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id:
        try:
            if answer.strip() in PYTHON_QUESTION_LIST[current_question_id-1]['options']:

                li=session.get('answers',[])
                li.append(str(answer).strip())
                session['answers']=li
                session.save()
            else:
                return (False,'Invalid answer')
        except Exception as e:
            return False,str(e)
    return True, ""
    


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id is None:
        current_question_id= 1
    else:
        current_question_id+=1
    response = (None,None)

    try:
       
        question=PYTHON_QUESTION_LIST[current_question_id-1]
        queston_text=question['question_text']
        options="<br>".join(question["options"])
       
        response = (queston_text+"<br>" +options, current_question_id)
        return response
    
    except IndexError:
        return response
        


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''

    score=0
    for i in range(len(li:=PYTHON_QUESTION_LIST)):
        if session.get('answers')[i]==li[i]['answer']:
            score+=1
    
    return  f"<b>You Scored {score}<b>"
    


