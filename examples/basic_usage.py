"""Basic usage examples for feature-flag-python."""

import asyncio
import os
from feature_flags import (
    initialize_client,
    is_enabled,
    get_feature,
    get_experiment,
    get_variant,
    ais_enabled,
    aget_experiment,
    feature_toggle,
    experiment_context,
    ExperimentVariant,
    cleanup_async_clients
)


def setup():
    """Setup the feature flag client."""
    # You can set the base URL via environment variable or directly
    os.environ["FEATURE_FLAG_BASE_URL"] = "http://localhost:8080"
    initialize_client()


def basic_feature_flag_example():
    """Basic feature flag usage."""
    print("=== Basic Feature Flag Example ===")

    # Simple on/off check
    if is_enabled("new-ui", default=False):
        print(" New UI is enabled")
    else:
        print(" New UI is disabled")

    # Feature with configuration
    feature = get_feature("recommendation-engine", default_enabled=True)
    if feature.enabled:
        max_items = feature.config.get("max_items", 5) if feature.config else 5
        print(f" Recommendations enabled with max {max_items} items")
    else:
        print(" Recommendations disabled")


def experiment_example():
    """A/B testing example."""
    print("\n=== A/B Testing Example ===")

    user_id = "user123"

    # Simple variant check
    variant = get_variant("checkout-flow", user_id, default_variant=ExperimentVariant.CONTROL)
    if variant == ExperimentVariant.TREATMENT:
        print(" User in treatment group - showing new checkout")
    else:
        print(" User in control group - showing old checkout")

    # Experiment with configuration
    experiment = get_experiment("pricing-test", user_id, default_variant=ExperimentVariant.CONTROL)
    if experiment.variant == ExperimentVariant.TREATMENT:
        discount = experiment.payload["discount"] if experiment.payload and "discount" in experiment.payload else 0.1
        print(f" Treatment: Apply {discount * 100}% discount")
    else:
        print(" Control: No discount")


def context_manager_example():
    """Context manager usage."""
    print("\n=== Context Manager Example ===")

    # Feature flag context
    with feature_toggle("dark-mode", default=False) as enabled:
        if enabled:
            print(" Dark mode is on")
        else:
            print(" Light mode is on")

    # Experiment context
    user_id = "user456"
    with experiment_context("search-algorithm", user_id) as experiment:
        if experiment.variant == ExperimentVariant.TREATMENT:
            algorithm = experiment.payload["algorithm"] if experiment.payload and "algorithm" in experiment.payload else "ml"
            print(f" Using {algorithm} search algorithm")
        else:
            print(" Using basic search algorithm")


async def async_example():
    """Async usage examples."""
    print("\n=== Async Example ===")

    # Async feature flag
    if await ais_enabled("async-processing", default=False):
        print(" Async processing enabled")
    else:
        print(" Sync processing enabled")

    # Async experiment
    user_id = "user789"
    experiment = await aget_experiment("notification-system", user_id)
    if experiment.variant == ExperimentVariant.TREATMENT:
        print(" Using new notification system")
    else:
        print(" Using old notification system")


def error_handling_example():
    """Error handling examples."""
    print("\n=== Error Handling Example ===")

    # Safe feature flag check with default
    safe_feature = is_enabled("experimental-feature", default=False)
    print(f"Experimental feature: {'enabled' if safe_feature else 'disabled'}")

    # With try-catch for more control
    try:
        risky_feature = is_enabled("risky-feature")
        print(f"Risky feature: {'enabled' if risky_feature else 'disabled'}")
    except Exception as e:
        print(f"Error checking risky feature: {e}")
        print("Falling back to safe default")


def main():
    """Run all examples."""
    setup()

    basic_feature_flag_example()
    experiment_example()
    context_manager_example()
    error_handling_example()

    # Run async example
    asyncio.run(async_example())

    # Cleanup
    asyncio.run(cleanup_async_clients())


if __name__ == "__main__":
    main()
