import os
def compileTable(mtt_id, var):
    static_weights =    [[5*var[0], var[1], var[2], var[3], var[3], var[2], var[1], 5*var[0]],
                        [ var[1], var[4], var[5], var[6], var[6], var[5], var[4], var[1]],
                        [ var[2], var[5], var[7], var[8], var[8], var[7], var[5], var[2]],
                        [ var[3], var[6], var[8], var[9], var[9], var[8], var[6], var[3]],
                        [ var[3], var[6], var[8], var[9], var[9], var[8], var[6], var[3]],
                        [ var[2], var[5], var[7], var[8], var[8], var[7], var[5], var[2]],
                        [ var[1], var[4], var[5], var[6], var[6], var[5], var[4], var[1]],
                        [ 5*var[0], var[1], var[2], var[3], var[3], var[2], var[1], 5*var[0]]]

    tables =  [0] * 10

    counter = 0
    weight_lists =  [[],[],[],[],[0, 0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0, 0],[0, 0, 0, 0, 0],[0, 0, 0, 0],[0, 0, 0]]
    for x in range(0, 4):
        weight_list = [0, 0, 0, 0, 0, 0, 0, 0]
        for y in range(0, 8):
            weight_list[y] = static_weights[x][y]
        
        weight_lists[counter] = weight_list
        counter += 1

    for x in range(0, 6):
        x1 = x
        y1 = 0
        while x1 < 8:
            weight_lists[counter][y1] = static_weights[x1][y1]
            x1 += 1
            y1 += 1
        counter += 1

    for counter in range(0, 10):
        if counter == 0:
            tables[counter] = create_table(weight_lists[counter], [var[10], var[11]/10, var[12]], True)
        else:
            tables[counter] = create_table(weight_lists[counter], [var[10], var[11]/10, var[12]], False)

    write_tables(tables, mtt_id)

def write_tables(tables, mtt_id):

    result = "from .hash_table import HashTable\ndef create_mobility_tables():\n    tables = [0]*10\n"
    for i in range(0,len(tables)):
        table_init = "    tables[%d] = HashTable()\n" % i
        result = result + table_init
        for key in tables[i].keys():
            value = tables[i][key]
            add_value = "    tables[%d].insert(%d, %f)\n" % (i, key, value)
            result = result + add_value
    result = result + "    return tables"
    os.remove("learning_alg/agents/agent"+str(mtt_id+1)+"/mobility_tables.py")
    f = open("learning_alg/agents/agent"+str(mtt_id+1)+"/mobility_tables.py", "a")
    f.write(result)
    f.close()

def create_table(weight_list, var, isSide):
    le = len(weight_list)
    result = {}
    for a0 in range(0,3):
        for a1 in range(0,3):
            for a2 in range(0,3):
                if le > 3:
                    for a3 in range(0,3):
                        if le > 4:
                            for a4 in range(0,3):
                                if le > 5:
                                    for a5 in range(0,3):
                                        if le > 6:
                                            for a6 in range(0,3):
                                                if le > 7:
                                                    for a7 in range(0,3):
                                                        key = compute_key([a0,a1,a2,a3,a4,a5,a6,a7])
                                                        value = compute_value([a0,a1,a2,a3,a4,a5,a6,a7], weight_list, var, isSide)
                                                        result[key] = value
                                                else:
                                                    key = compute_key([a0,a1,a2,a3,a4,a5,a6,0])
                                                    value = compute_value([a0,a1,a2,a3,a4,a5,a6,0], weight_list, var, isSide)
                                                    result[key] = value
                                        else:
                                            key = compute_key([a0,a1,a2,a3,a4,a5,0,0])
                                            value = compute_value([a0,a1,a2,a3,a4,a5,0,0], weight_list, var, isSide)
                                            result[key] = value
                                else:
                                    key = compute_key([a0,a1,a2,a3,a4,0,0,0])
                                    value = compute_value([a0,a1,a2,a3,a4,0,0,0], weight_list, var, isSide)
                                    result[key] = value
                        else:
                            key = compute_key([a0,a1,a2,a3,0,0,0,0])
                            value = compute_value([a0,a1,a2,a3,0,0,0,0], weight_list, var, isSide)
                            result[key] = value
                else:
                    key = compute_key([a0,a1,a2,0,0,0,0,0])
                    value = compute_value([a0,a1,a2,0,0,0,0,0], weight_list, var, isSide)
                    result[key] = value
    return result

def compute_key(el_list):
    return el_list[0] + el_list[1]*3 + el_list[2]*9 + el_list[3]*27 + el_list[4]*81 + el_list[5]*243 + el_list[6]*729 + el_list[7]*2187

EMPTY = 0
BLACK = 1
WHITE = 2

def compute_value(el_list, weight_list, var, isSide):
    result = 0.0
    last_el = el_list[0]

    if last_el == BLACK:
        result += weight_list[0]
    elif last_el == WHITE:
        result -= weight_list[0]

    for counter in range(1, len(weight_list)):
        el = el_list[counter]

        if el == BLACK:
            result += weight_list[counter]
            if last_el == BLACK:
                result -= var[0]
            elif last_el == WHITE:
                result -= 0
            else:
                result -= var[1]*weight_list[counter - 1]
    
        elif el == WHITE:
            result -= weight_list[counter]
            if last_el == BLACK:
                result += 0
            elif last_el == WHITE:
                result += var[0]
            else:
                result += var[1]*weight_list[counter - 1]
        
        else:
            if last_el == BLACK:
                result -= var[1]*weight_list[counter]
            elif last_el == WHITE:
                result += var[1]*weight_list[counter]
        last_el = el
    
    if isSide == True:
        counter = 0
        if el_list[0] == BLACK:
            for counter in range(1, len(weight_list)):
                if el_list[counter] == BLACK:
                    result += var[2]
                else:
                    break
        elif el_list[0] == WHITE:
            for counter in range(1, len(weight_list)):
                if el_list[counter] == WHITE:
                    result -= var[2]
                else:
                    break
        if counter != 7:
            if el_list[7] == BLACK:
                for counter in range(1, len(weight_list)):
                    if el_list[7 - counter] == BLACK:
                        result += var[2]
                    else:
                        break
            elif el_list[7] == WHITE:
                for counter in range(1, len(weight_list)):
                    if el_list[7 - counter] == WHITE:
                        result -= var[2]
                    else:
                        break

    return result

if __name__ == "__main__":
    compileTable(20, [26.4182921 ,  3.61579667, 16.91354517,  5.44322345, -9.01984636,
       -9.50027461,  0.62327498,  7.08086365,  1.54969233, -1.9107416 ,
        0.24364641, 10.95576195, 11.03142108])