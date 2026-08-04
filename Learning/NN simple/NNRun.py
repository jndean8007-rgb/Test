import Neural_Net
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split


def main():
    housing = fetch_california_housing(as_frame=True)

    X_train, X_test, y_train, y_test = train_test_split(
        housing.data,
        housing.target,
        test_size=0.2,
        random_state=42
    )

    net = Neural_Net.Neuralnet(
        data=X_train,
        target=y_train,
        layers=(8, 8),
        sgd_spec=(20, 20, 0.05),
        output_type="Quant"
    )

    print(
        "Prediction before training:",
        net.predict(X_test.iloc[0])
    )

    net.train()

    print(
        "Prediction after training:",
        net.predict(X_test.iloc[0])
    )

    print(
        "Actual target:",
        y_test.iloc[0]
    )


if __name__ == "__main__":
    main()