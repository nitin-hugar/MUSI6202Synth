from itertools import chain
import math


parser = argparse.ArgumentParser(description='Calculate volume of the cylinder')
parser.add_argument('-r', '--radius', type=int, metavar='', required=True, help='Radius of Cylinder')
parser.add_argument('-H', '--height', type=int, metavar='', required=True, help='Height of Cylinder')
group = parser.add_mutually_exclusive_group()
group.add_argument('-q', '--quite', action='store_true', help='print quite')
group.add_argument('-v', '--verbose', action='store_true', help='print verbose')
args = parser.parse_args()


def cylinder_volume(radius, height):
  vol = (math.pi) * (radius ** 2) * height
  return vol

if __name__ == '__main__':
  volume = cylinder_volume(args.radius, args.height)
  if args.quite:
    print (volume)
  elif args.verbose:
    print ("Volume of a cylinder with radius %s and height %s is %s" %(args.radius, args.height, volume))
  else:
    print ("Volume of cylinder = %s" % volume)