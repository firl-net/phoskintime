import numpy as np
from kinopt.evol.objfn import estimated_series
from kinopt.evol.config.logconf import setup_logger

logger = setup_logger()


def extract_parameters(P_initial, gene_psite_counts, K_index, optimized_params):
    """
    Function to extract alpha and beta values from the optimized parameters.

    Args:
        P_initial (dict): Dictionary containing initial parameters for each gene-psite pair.
        gene_psite_counts (list): List of counts for each gene-psite pair.
        K_index (dict): Dictionary mapping kinases to their respective psite pairs.
        optimized_params (list): List of optimized parameters.

    Returns:
        alpha_values (dict): Dictionary containing alpha values for each gene-psite pair.
        beta_values (dict): Dictionary containing beta values for each kinase-psite pair.
    """
    alpha_values = {}
    alpha_start = 0
    for idx, count in enumerate(gene_psite_counts):
        gene, psite = list(P_initial.keys())[idx]
        kinases = P_initial[(gene, psite)]['Kinases']
        alpha_values[(gene, psite)] = dict(zip(kinases, optimized_params[alpha_start:alpha_start + count]))
        alpha_start += count

    # Extract betas for kinase-psite
    beta_values = {}
    beta_start = sum(gene_psite_counts)
    for kinase, kinase_psites in K_index.items():
        for psite, _ in kinase_psites:
            count = 1  # Each psite in beta_counts has a count of 1
            beta_values[(kinase, psite)] = optimized_params[beta_start:beta_start + count]
            beta_start += count
            # Display optimized values
    logger.info("Optimized Alpha Values:")
    for (gene, psite), kinases in alpha_values.items():
        logger.info(f"Protein {gene}, Psite {psite}:")
        for kinase, value in kinases.items():
            logger.info(f"  Kinase {kinase}: {value}")

    logger.info("Optimized Beta Values:")
    for (kinase, psite), value in beta_values.items():
        logger.info(f"Kinase {kinase}, Psite {psite}: {value}")
    return alpha_values, beta_values


def compute_metrics(optimized_params: np.ndarray, P_initial: dict, P_initial_array: np.ndarray,
                    K_index: dict, K_array: np.ndarray,
                    gene_psite_counts: list, beta_counts: dict, n: int):
    """
    Function to compute error metrics for the estimated series.

    Args:
        optimized_params (list): List of optimized parameters.
        P_initial (dict): Dictionary containing initial parameters for each gene-psite pair.
        P_initial_array (np.ndarray): Array of initial parameters.
        K_index (dict): Dictionary mapping kinases to their respective psite pairs.
        K_array (np.ndarray): Array of kinases.
        gene_psite_counts (list): List of counts for each gene-psite pair.
        beta_counts (dict): List of counts for each kinase-psite pair.
        n (int): Number of samples.

    Returns:
        P_estimated (np.ndarray): Estimated series.
        residuals (np.ndarray): Residuals between initial and estimated series.
        mse (float): Mean Squared Error.
        rmse (float): Root Mean Squared Error.
        mae (float): Mean Absolute Error.
        mape (float): Mean Absolute Percentage Error.
        r_squared (float): R-squared value.
    """
    P_estimated = estimated_series(
        optimized_params, P_initial, K_index, K_array, gene_psite_counts, beta_counts
    )
    residuals = P_initial_array - P_estimated
    mse = np.sum((residuals) ** 2) / n
    rmse = np.sqrt(mse)
    mae = np.mean(np.abs(residuals))
    mape = np.mean(np.abs(residuals / P_initial_array)) * 100
    r_squared = 1 - (np.sum((residuals) ** 2) / np.sum((P_initial_array - np.mean(P_initial_array)) ** 2))
    logger.info("--- Error Metrics ---")
    logger.info(f"Mean Squared Error (MSE): {mse:.4f}")
    logger.info(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    logger.info(f"Mean Absolute Error (MAE): {mae:.4f}")
    logger.info(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
    logger.info(f"R-squared (R^2): {r_squared:.4f}")
    return P_estimated, residuals, mse, rmse, mae, mape, r_squared
