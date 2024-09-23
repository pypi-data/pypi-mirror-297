from typing import Callable, Optional

import numpy as np
from numba import jit
import numba
import pandas as pd
import scipy.optimize as opt

import rangekeeper as rk


class Financial:

    @staticmethod
    def interest(
            amount: float,
            rate: float,
            balance: rk.flux.Flow,
            frequency: rk.duration.Type,
            capitalized: bool = False) -> rk.flux.Flow:
        """
        Calculate interest expense on a loan or other interest-bearing liability.
        Make sure the rate is consistent with the frequency
        """

        balance = balance.resample(frequency=frequency)

        interest_amounts = rk.formula.Financial._calculate_interest(
            amount=np.float64(amount),
            balance=numba.typed.List(balance.movements.to_list()),
            rate=np.float64(rate),
            capitalized=capitalized)

        return rk.flux.Flow(
            name='Interest',
            movements=pd.Series(
                data=interest_amounts,
                index=balance.movements.index),
            units=balance.units)

    @staticmethod
    @numba.jit
    def _calculate_interest(
            amount: np.float64,
            balance: numba.typed.List,
            rate: np.float64,
            capitalized: bool = False) -> numba.typed.List:

        utilized = numba.typed.List()
        interest = numba.typed.List()
        accrued = numba.typed.List()

        for i in range(len(balance)):
            utilized.append(amount - balance[i])

            if capitalized:
                accrued_amount = 0 if i == 0 else accrued[-1]
                interest_amount = 0 if np.isclose(utilized[i], 0) else (utilized[i] + accrued_amount) * rate
                interest.append(interest_amount)
                accrued.append(sum(interest))
            else:
                interest_amount = 0 if np.isclose(utilized[i], 0) else utilized[i] * rate
                interest.append(interest_amount)

        return interest

    @staticmethod
    def capitalized_interest(
            transactions: rk.flux.Stream,
            rate: float) -> (rk.flux.Stream, rk.flux.Flow):
        """
        Calculate capitalized interest on a series of transactions.
        Returns a balance (Stream with "Starting" & "Ending" values) and an "Interest" Flow
        """
        starting, ending, interest = rk.formula.Financial._calc_capitalized_interest(
            transactions=numba.typed.List(transactions.sum().movements.to_list()),
            rate=np.float64(rate))

        units = transactions.sum().units
        balance = rk.flux.Stream(
            name=transactions.name,
            flows=[
                rk.flux.Flow.from_sequence(
                    sequence=transactions.frame.index,
                    data=record,
                    units=units,
                    name=name)
                for record, name in zip((starting, ending), ('Starting', 'Ending'))
            ],
            frequency=transactions.frequency)

        interest = rk.flux.Flow.from_sequence(
            sequence=transactions.frame.index,
            data=interest,
            units=units,
            name='Interest')

        return balance, interest



    @staticmethod
    # @numba.jit
    def _calc_capitalized_interest(
            transactions: numba.typed.List,
            rate: np.float64):

        startings = numba.typed.List.empty_list(numba.float64)
        endings = numba.typed.List.empty_list(numba.float64)
        interests = numba.typed.List.empty_list(numba.float64)
        # accrued = numba.typed.List()

        for i in range(len(transactions)):
            if i == 0:
                startings.append(0)
            else:
                startings.append(endings[-1])
            principal = startings[i] + transactions[i]
            interest = (abs(principal) * rate) / (1 - rate) if principal < 0 else 0
            endings.append(principal - interest)
            interests.append(interest)

        return startings, endings, interests


        # for i in range(len(transactions)):
        #     if i == 0:
        #         starting.append(0)
        #         # principal = transactions[i]
        #     else:
        #         starting.append(ending[-1])
        #         # principal = starting[i] + transactions[i]
        #         # print('Principal at {0}: '.format(i) + str(principal))
        #     if starting < 0:
        #         draw = abs() / (1 - rate) # Since we are capitalizing interest, and our draw must include interest to pay on the draw. Derived from i = r * (P + i)
        #         print('Draw at {0}: '.format(i) + str(draw))
        #
        #         ending.append(starting[i] - draw)
        #
        #         interest.append(draw * rate)
        #     else:
        #         ending.append(principal)
        #         interest.append(0)
        #
        # return starting, ending, interest


    @staticmethod
    def balance(
            starting: float,
            transactions: rk.flux.Stream,
            name: str = None) -> (rk.flux.Stream, rk.flux.Flow):
        """
        Calculate the balance of a financial account given a starting balance and a series of transactions.
        Assumes the ending balance can never be negative.
        Returns a tuple of:
        - a Stream with two Flows: "Start Balance" and "End Balance"
        - the residual Flow of any remaining transactions
        """

        starting = numba.typed.List([np.float64(starting)])
        transaction_amounts = numba.typed.List(transactions.sum().movements.to_list())

        balance, remaining = rk.formula.Financial._calculate_balance(
            starting=starting,
            transactions=transaction_amounts)

        flows = [
            rk.flux.Flow.from_sequence(
                sequence=transactions.frame.index,
                data=record,
                units=transactions.sum().units,
                name=name)
            for record, name in zip(balance, ('Start Balance', 'End Balance'))
        ]

        statement = rk.flux.Stream(
            name=name,
            flows=flows,
            frequency=transactions.frequency)

        remaining = rk.flux.Flow.from_sequence(
            sequence=transactions.frame.index,
            data=remaining,
            units=transactions.sum().units,
            name='Remaining Transactions')

        return statement, remaining

    @staticmethod
    @numba.jit
    def _calculate_balance(
            starting: numba.typed.List,
            transactions: numba.typed.List) -> numba.typed.List:

        ending = numba.typed.List.empty_list(numba.float64)
        remaining = numba.typed.List.empty_list(numba.float64)
        for i in range(len(transactions)):
            end = float(starting[-1] + transactions[i])
            if (end >= 0) or (np.isclose(end, 0)):
                ending.append(end)
                remaining.append(0)
            else:
                ending.append(0)
                remaining.append(transactions[i])
            starting.append(ending[-1])
        return ((starting[:-1], ending), remaining)

    @staticmethod
    def required_principal(
            desired: float,
            capitalized_cost: Callable[[float, dict], float],
            params: dict = None) -> float:
        """

        """
        def solve(principal):
            required = principal[0]
            price = capitalized_cost(required, params)
            return [abs(desired - (required - price))]

        result = opt.root(solve, [desired], method='lm')
        return float(result.x)