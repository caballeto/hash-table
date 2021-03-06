from sys import argv
from chainedhash import ChainedHash
from openhash import OpenHash
from hashes import hashes

def readData(infile):
  with open(infile) as fin:
    amount = int(fin.readline().split(' ')[0])
    data = [int(num) for num in fin]
    arr = data[:amount]
    sums = data[amount:]
  return arr, sums

def getResult(arr, sums, table):
  result = []

  for el in sums:
    for num in arr:
      if el - num in table:
        result.append([num, el - num])
        break
    else:
      result.append([0, 0])

  return result

if __name__ == '__main__':
  infile, k = argv[1], int(argv[2])
  outfile = 'ip71_teliman_06_output.txt'
  golden = (1 + 5 ** 0.5) / 2

  arr, sums = readData(infile)

  if k == 1: table = ChainedHash(len(arr) * 3, hashes['divide'])
  elif k == 2: table = ChainedHash(len(arr) * 3, hashes['multiply'])
  elif k == 3: table = OpenHash(len(arr) * 3, hashes['linear'])
  elif k == 4: table = OpenHash(len(arr) * 3, hashes['quadratic'])
  elif k == 5: table = OpenHash(len(arr) * 3, hashes['double'])
  else: raise Exception('Unknown \'k\' argument')

  for num in arr:
    table[num] = num

  result = getResult(arr, sums, table)

  with open(outfile, 'w') as fout:
    fout.write('%d\n' % table.collisions)
    fout.write('\n'.join('%d %d' % tuple(nums) for nums in result))
