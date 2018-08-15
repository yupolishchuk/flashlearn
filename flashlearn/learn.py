import time, datetime

from flask import Blueprint
from flashlearn.db import connect
from flask import render_template
from flask import request
from flask import jsonify


bp = Blueprint('learn', __name__)

engine = connect()


@bp.route('/learn/', methods=['GET'])
def learn():
    return render_template('learn.html')


@bp.route('/give_card', methods=['POST'])
def give_card():
    card_id = int(request.form.get("card_id"))
    action = request.form.get('action')

    engine = connect()

    '''
    Приоритет выдачи карт
    Выбрать все из выбранной колоды которые
        отвечал больше дня назад + начиная из самого низкого уровня
        выбираем все обновленные сегодня но больше часа назад + начиная из самого низкого уровня
        выбираем все обновленные меньше часа назад + начная из самого низкого уровня
        Когда карты закончились - выводим сообщение: Колода закончилась, с возможностью начать заново
    '''

    if action == 'give_first':
        sql = 'SELECT * FROM `flashcard` WHERE level = (SELECT MIN(level) FROM `flashcard`)'
        card = engine.execute(sql).first()

        return jsonify([str(card[0]), str(card[1]), str(card[2]), str(card[4])])

    elif action == 'give_next':
        current = str(card_id)
        current_level = engine.execute("SELECT level FROM flashcard WHERE id = " + current).first()

        next_id = engine.execute(
            "SELECT MIN(id) FROM flashcard "
            "WHERE id > " + current + " AND level = " + str(current_level[0])
        ).first()

        if next_id[0] is None:
            sql = 'SELECT MIN(level) FROM `flashcard` WHERE `level` > ' + str(current_level[0])
            next_level = engine.execute(sql).first()
            next_id = engine.execute(
                "SELECT MIN(id) FROM flashcard "
                "WHERE level = " + str(next_level[0])).first()

        # return result
        if next_id[0]:
            sql = 'SELECT * FROM `flashcard` WHERE id = ' + str(next_id[0])
            card = engine.execute(sql).first()
            return jsonify([str(card[0]), str(card[1]), str(card[2]), str(card[4])])
        else:
            return 'card not found'

    elif action == 'give_prev':
        current = str(card_id)
        current_level = engine.execute("SELECT level FROM flashcard WHERE id = " + current).first()

        prev_id = engine.execute(
            "SELECT MAX(id) FROM flashcard "
            "WHERE id < " + current + " AND level = " + str(current_level[0])
        ).first()

        if prev_id[0] is None:
            prev_level = engine.execute('SELECT MAX(level) FROM `flashcard` WHERE `level` < ' + str(current_level[0])).first()
            prev_id = engine.execute(
                "SELECT MAX(id) FROM flashcard "
                "WHERE level = " + str(prev_level[0])).first()

        # return result
        if prev_id[0]:
            sql = 'SELECT * FROM `flashcard` WHERE id = ' + str(prev_id[0])
            card = engine.execute(sql).first()

            return jsonify([str(card[0]), str(card[1]), str(card[2]), str(card[4])])
        else:
            return 'card not found'


@bp.route("/set_level", methods=["POST"])
def update_level():
    # TODO exception handling and sending operation status

    card_id = request.form.get('card_id')
    level = request.form.get('level')

    sql = 'UPDATE `flashcard` SET `level` = ' + str(level) + ' WHERE `flashcard`.`id` = ' + str(card_id)
    engine.execute(sql)
    return 'success'


def current_timestamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st
