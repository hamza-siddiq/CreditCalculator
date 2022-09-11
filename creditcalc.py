import argparse
import math
import sys

parser = argparse.ArgumentParser(
    description="This program is a loan calculator for differentiated and annuity payments")
parser.add_argument("-t", "--type",
                    choices=["annuity", "diff"],
                    help='Enter the type of payment: "annuity" for annuity or "diff" for differentiated')
parser.add_argument("-pt", "--payment",
                    help="Enter the payment for annuity")
parser.add_argument("-pl", "--principal",
                    help="Enter the principal amount")
parser.add_argument("-pd", "--periods",
                    help="The number of months needed to repay the loan")
parser.add_argument("-i", "--interest",
                    help="The interest rate specified without a percentage sign")

args = parser.parse_args()

if (args.type != "annuity" and args.type != "diff") \
        or (args.type == "diff" and args.payment) \
        or not args.interest \
        or len(sys.argv) < 5 \
        or (args.payment is not None and float(args.payment) < 0)\
        or (args.principal is not None and float(args.principal) < 0)\
        or (args.periods is not None and float(args.periods) < 0):
    print("Incorrect parameters")
    exit()

if args.principal:
    principal = float(args.principal)
if args.periods:
    periods = int(args.periods)
if args.payment:
    payment = float(args.payment)

interest = float(args.interest)

if args.type == "diff":
    periods = int(args.periods)
    principal = float(args.principal)

    nominal_interest = interest / (12 * 100)
    total_payment = 0
    for month in range(1, periods+1):
        diff_payment = math.ceil((principal / periods) + nominal_interest * (principal - (principal * (month - 1)) / periods))
        print(f"Month {month}: payment is {diff_payment}")
        total_payment += diff_payment
    over_payment = total_payment - principal
    print(f"Overpayment = {over_payment}")

elif args.type == "annuity":
    nominal_interest = interest / (12 * 100)
    if args.principal and args.payment and args.interest:
        principal = float(args.principal)
        payment = float(args.payment)

        periods = math.ceil(math.log(payment /
                                          (payment - (nominal_interest * principal)),
                                          1 + nominal_interest))
        years = periods // 12
        months = periods % 12
        overpayment = periods * payment - principal

        if years == 1 and months == 1:
            print("It will take 1 year and 1 month to repay this loan!")
        elif years == 1 and months == 0:
            print("It will take 1 year to repay this loan!")
        elif years == 0 and months == 1:
            print("It will take 1 month to repay this loan!")
        elif years == 0 and months != 1:
            print(f"It will take {months} months to repay this loan!")
        elif years != 1 and months == 0:
            print(f"It will take {years} years to repay this loan!")
        else:
            print(f"It will take {years} years and {months} months to repay this loan!")
        print(f"Overpayment = {overpayment}")

    elif args.principal and args.periods and args.interest:
        principal = float(args.principal)
        periods = int(args.periods)

        nominal_interest = (interest / 100) / 12
        payment = math.ceil((principal * nominal_interest * pow((1 + nominal_interest), periods)) /
                                    (pow((1 + nominal_interest), periods) - 1))
        overpayment = periods * payment - principal
        print(f"Your annuity payment = {payment}!")
        print(f"Overpayment = {overpayment}")

    elif args.payment and args.periods and args.interest:
        payment = float(args.payment)
        periods = int(args.periods)

        nominal_interest = (interest / 100) / 12
        principal = math.ceil(payment /
                                   ((nominal_interest * pow((1 + nominal_interest), periods)) / (
                                           pow((1 + nominal_interest), periods) - 1)))
        overpayment = periods * payment - principal
        print(f"Your loan principal = {principal}!")
        print(f"Overpayment = {overpayment}")