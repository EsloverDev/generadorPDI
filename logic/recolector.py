def actividadYaAsignada(cursor, codalu, codcur, anomat, numper, codeva, nroopo, codtem, nrosec):
    query = """
        SELECT 1
        FROM alplades
        WHERE codalu = %s AND codcur = %s AND anomat = %s AND numper = %s AND codeva = %s AND nroopo = %s AND codtem = %s AND nrosec = %s
        LIMIT 1
    """
    cursor.execute(query, (codalu, codcur, anomat, numper, codeva, nroopo, codtem, nrosec))
    return cursor.fetchone() is not None
