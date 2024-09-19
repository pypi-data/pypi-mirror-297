import os
import argparse
import logging
from .sequence_processing import load_sequences, preprocess_sequences, create_encodings
from .make_predictions import (
    predict_binary,
    predict_family,
    predict_subfamily,
    predict_metabolic_important
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main(input_file: str, output_dir: str, preprocess: bool = True, gpu: int = 2) :
    df_sequences = load_sequences(input_file)
    
    if preprocess:
        logging.info("Preprocessing sequences and creating encodings")
        df_sequences = preprocess_sequences(df_sequences)

    encodings, labels = create_encodings(df_sequences, input_file)

    df_binary_predictions, binary_labels = predict_binary(encodings, labels)
    df_family_predictions = predict_family(encodings, labels)
    df_subfamily_predictions = predict_subfamily(encodings, labels)
    df_metabolic_predictions = predict_metabolic_important(encodings, labels)

    df_merged = df_binary_predictions.merge(df_family_predictions, on='Accession', how='left')
    df_merged = df_merged.merge(df_subfamily_predictions, on='Accession', how='left')
    df_merged = df_merged.merge(df_metabolic_predictions, on='Accession', how='left')

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, "final_predictions.csv")
    df_merged.to_csv(output_file, index=False)
    logging.info(f"All predictions saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the prediction pipeline")
    parser.add_argument('--input_dir', type=str, required=True, help='Input file path')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory path')
    parser.add_argument('--gpu', type=int, default=2, help='GPU index to use')
    parser.add_argument('--nopreprocess', action='store_false', dest='preprocess', help='Disable preprocessing of sequences')
    args = parser.parse_args()

    main(args.input_dir, args.output_dir, args.gpu, args.preprocess)