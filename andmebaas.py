"""Database module for task management."""
import sqlite3


def loo_andmebaas():
    '''Loob andmebaasi kui seda ei ole'''
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()  # aitab andmebaasist asju võtta

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nimi TEXT NOT NULL,
            kestvus INTEGER NOT NULL,
            kolonn INTEGER DEFAULT NONE,
            rida INTEGER DEFAULT NONE,
            kirjeldus TEXT DEFAULT '',
            tüüp TEXT DEFAULT 'Määramata',
            värv TEXT DEFAULT '#FFC0CB'

        );
    ''')
    # default värv on roosa
    # Kestvuses peab olema millal
    connection.commit()
    connection.close()


def muuda_toimumisaega(task_id, kolonn, rida):
    '''Lisab eventile aja'''
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute(
        'UPDATE tasks SET kolonn = ?, rida = ? WHERE id = ?', (kolonn, rida, task_id))
    connection.commit()
    connection.close()


def saa_task():
    '''Saab viimase taski andmebaasist'''
    connection = sqlite3.connect('andmed.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * from tasks ORDER BY id DESC LIMIT 1')
    rida = cursor.fetchone()

    andmed = dict(rida)
    connection.close()
    return andmed


def saa_task_id(task_id):
    '''Saab taski ID järgi andmebaasist'''
    connection = sqlite3.connect('andmed.db')
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()
    cursor.execute('SELECT * from tasks WHERE id = ?', (task_id,))
    rida = cursor.fetchone()
    if rida:
        andmed = dict(rida)
    else:
        andmed = None
    connection.close()
    return andmed


def saa_taskid():
    '''Saab kõik taskid andmebaasist'''
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM tasks")  # võtab kõik andmed.db-st
    colnames = [description[0]
                for description in cursor.description]  # saab headerid
    read = cursor.fetchall()  # siin on need võetud andmed
    andmed = []
    for rida in read:
        andmed.append(dict(zip(colnames, rida)))  # sõnastikuks
    connection.close()
    return andmed


def lisa_task(nimi, kestvus, kirjeldus, tüüp, värv, rida, kolonn):
    '''See lisab taski andmebaasi'''
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute(
        'INSERT INTO tasks (nimi,kestvus, kirjeldus, tüüp, värv, rida, kolonn) '
        'VALUES (?,?,?,?,?, ?,?)',
        (nimi, kestvus, kirjeldus, tüüp, värv, rida, kolonn))
    connection.commit()
    connection.close()


def kas_task_olemas(nimi, rida, kolonn):
    '''Kontrollib kas task sama nimega ja asukohaga juba eksisteerib.'''
    connection = sqlite3.connect('andmed.db')
    cursor = connection.cursor()
    cursor.execute(
        'SELECT id FROM tasks WHERE nimi = ? AND rida = ? AND kolonn = ?',
        (nimi, rida, kolonn))
    result = cursor.fetchone()
    connection.close()
    return result is not None
