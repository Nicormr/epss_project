"""Environmental flow targets (sheet eq. 9)."""


def eflow_targets(inflow, fraction=0.10):
    """Target e-flow (hm³/month): fraction x mean inflow of the same calendar month.

    inflow: pd.Series (hm³/month, monthly DatetimeIndex). Returns a Series on the same index.
    """
    # TODO: E-flow target (sheet eq. 9): fraction x mean inflow of the same calendar month (hint:
    #       groupby(index.month).transform('mean')).
    # In: inflow (pd.Series, hm³/month), fraction (-)
    # Out: pd.Series of targets (hm³/month), same index
    raise NotImplementedError("E-flow target (sheet eq. 9): fraction x mean inflow of the same calendar month (hint: groupby(index.month).transform('mean')).")
