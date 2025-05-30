import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from tfopt.local.config.constants import OUT_FILE


def save_results_to_excel(
        gene_ids, tf_ids,
        final_alpha, final_beta, psite_labels_arr,
        expression_matrix, predictions,
        objective_value,
        reg_map,
        filename=OUT_FILE
):
    """
    Save the optimization results to an Excel file.

    Args:
        gene_ids (list): List of gene identifiers.
        tf_ids (list): List of TF identifiers.
        final_alpha (np.ndarray): Final alpha values.
        final_beta (np.ndarray): Final beta values.
        psite_labels_arr (list): List of phosphorylation site labels.
        expression_matrix (np.ndarray): Observed expression levels.
        predictions (np.ndarray): Predicted expression levels.
        objective_value (float): Objective value from optimization.
        reg_map (dict): Mapping of genes to regulators.
        filename (str): Path to the output Excel file.
    """
    # --- Alpha Values ---
    alpha_rows = []
    n_genes, n_reg = final_alpha.shape
    for i in range(n_genes):
        gene = gene_ids[i]
        actual_tfs = [tf for tf in reg_map[gene] if tf in tf_ids]
        for j, tf_name in enumerate(actual_tfs):
            alpha_rows.append([gene, tf_name, final_alpha[i, j]])
    df_alpha = pd.DataFrame(alpha_rows, columns=["mRNA", "TF", "Value"])

    # --- Beta Values ---
    beta_rows = []
    for i, tf in enumerate(tf_ids):
        beta_vec = final_beta[i]
        beta_rows.append([tf, "", beta_vec[0]])  # Protein beta
        for j in range(1, len(beta_vec)):
            beta_rows.append([tf, psite_labels_arr[i][j - 1], beta_vec[j]])
    df_beta = pd.DataFrame(beta_rows, columns=["TF", "PSite", "Value"])

    # --- Residuals ---
    residuals = expression_matrix - predictions
    df_residuals = pd.DataFrame(residuals, columns=[f"x{j + 1}" for j in range(residuals.shape[1])])
    df_residuals.insert(0, "mRNA", gene_ids)

    # --- Observed ---
    df_observed = pd.DataFrame(expression_matrix, columns=[f"x{j + 1}" for j in range(expression_matrix.shape[1])])
    df_observed.insert(0, "mRNA", gene_ids)

    # --- Estimated ---
    df_estimated = pd.DataFrame(predictions, columns=[f"x{j + 1}" for j in range(predictions.shape[1])])
    df_estimated.insert(0, "mRNA", gene_ids)

    # --- Optimization Results ---
    y_true = expression_matrix.flatten()
    y_pred = predictions.flatten()
    mse = mean_squared_error(y_true, y_pred)
    mae = mean_absolute_error(y_true, y_pred)
    mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
    r2 = r2_score(y_true, y_pred)
    df_metrics = pd.DataFrame([
        ["Objective Value", objective_value],
        ["MSE", mse],
        ["MAE", mae],
        ["MAPE", mape],
        ["R^2", r2],
    ], columns=["Metric", "Value"])

    with pd.ExcelWriter(filename, engine='xlsxwriter') as writer:
        df_alpha.to_excel(writer, sheet_name="Alpha Values", index=False)
        df_beta.to_excel(writer, sheet_name="Beta Values", index=False)
        df_residuals.to_excel(writer, sheet_name="Residuals", index=False)
        df_observed.to_excel(writer, sheet_name="Observed", index=False)
        df_estimated.to_excel(writer, sheet_name="Estimated", index=False)
        df_metrics.to_excel(writer, sheet_name="Optimization Results", index=False)
