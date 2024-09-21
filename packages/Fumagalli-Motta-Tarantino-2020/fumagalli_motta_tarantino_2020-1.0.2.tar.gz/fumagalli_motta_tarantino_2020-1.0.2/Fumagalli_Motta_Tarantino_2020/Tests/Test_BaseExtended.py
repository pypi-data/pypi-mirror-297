import Fumagalli_Motta_Tarantino_2020.Tests.Test_Base as Test
import Fumagalli_Motta_Tarantino_2020 as FMT20


class TestCournotCompetition(Test.TestOptimalMergerPolicy):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.CournotCompetition.
    """

    def setUp(self) -> None:
        self.calculate_properties_profits_consumer_surplus()

    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.CournotCompetition(**kwargs)

    def calculate_properties_profits_consumer_surplus(self) -> None:
        """
        Calculates the properties defined by the cournot competition.

        As default gamma is assumed to be 0.3.
        """
        self.test_incumbent_profit_without_innovation = 0.25
        self.test_cs_without_innovation = 0.125

        self.test_incumbent_profit_with_innovation = 1 / 2.6
        self.test_cs_with_innovation = 1 / 5.2

        self.test_incumbent_profit_duopoly = 1 / (2.3**2)
        self.test_startup_profit_duopoly = self.test_incumbent_profit_duopoly
        self.test_cs_duopoly = 1.3 / (2.3**2)

    def get_welfare_value(self, market_situation: str, **kwargs) -> float:
        if market_situation == "duopoly":
            return (
                self.test_cs_duopoly
                + self.test_startup_profit_duopoly
                + self.test_incumbent_profit_duopoly
            )
        if market_situation == "without_innovation":
            return (
                self.test_cs_without_innovation
                + self.test_incumbent_profit_without_innovation
            )
        if market_situation == "with_innovation":
            return (
                self.test_cs_with_innovation
                + self.test_incumbent_profit_with_innovation
            )

    def test_properties_profits_consumer_surplus(self):
        self.setupModel()
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_without_innovation, self.model.cs_without_innovation
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_without_innovation,
                self.model.incumbent_profit_without_innovation,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_duopoly,
                self.model.cs_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_duopoly,
                self.model.incumbent_profit_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_startup_profit_duopoly,
                self.model.startup_profit_duopoly,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_cs_with_innovation,
                self.model.cs_with_innovation,
            )
        )
        self.assertTrue(
            self.are_floats_equal(
                self.test_incumbent_profit_with_innovation,
                self.model.incumbent_profit_with_innovation,
            )
        )

    def test_intermediate_optimal_merger_policy(self):
        self.setupModel(
            development_costs=0.12,
            startup_assets=0.09,
            success_probability=0.87,
            private_benefit=0.09,
            gamma=0.12,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.get_optimal_merger_policy(),
        )
        self.assertTrue(self.model.is_intermediate_optimal())

    def test_string_representation(self):
        self.setupModel(gamma=0.3)
        self.assertEqual(
            "Merger Policy: Strict\n"
            "Is start-up credit rationed?: False\n"
            "Type of early takeover attempt: No bid\n"
            "Is the early takeover approved?: False\n"
            "Does the owner attempt the development?: True\n"
            "Is the development successful?: True\n"
            "Type of late takeover attempt: No bid\n"
            "Is the late takeover approved?: False\n"
            "Optimal merger policy: Strict",
            str(self.model),
        )

    def test_laissez_faire_optimal_merger_policy(self):
        # laissez-faire is never optimal -> dominated by strict
        self.setupModel()
        self.assertFalse(self.model.is_laissez_faire_optimal())

    def test_tolerated_harm_strict(self):
        self.setupModel()
        self.assertEqual(0, self.model.tolerated_harm)

    def test_tolerated_harm_intermediate_late_takeover_allowed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
        )
        self.assertTrue(
            self.are_floats_equal(
                (1 - 0.5070508811267713)
                * (
                    0.7
                    * (
                        self.get_welfare_value("duopoly")
                        - self.get_welfare_value("without_innovation")
                    )
                    - 0.1
                ),
                self.model.tolerated_harm,
            )
        )

    def test_tolerated_harm_intermediate_late_takeover_prohibited(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed
        )
        self.assertEqual(
            self.get_welfare_value("duopoly")
            - self.get_welfare_value("with_innovation"),
            self.model.tolerated_harm,
        )

    def test_tolerated_harm_laissez_faire(self):
        self.setupModel(merger_policy=FMT20.MergerPolicies.Laissez_faire)
        self.assertEqual(float("inf"), self.model.tolerated_harm)


class TestPerfectInformation(Test.TestOptimalMergerPolicy):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.PerfectInformation.
    """

    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.PerfectInformation(**kwargs)

    def test_tolerated_harm_intermediate_late_takeover_allowed(self):
        self.assertRaises(
            FMT20.Exceptions.MergerPolicyNotAvailable,
            lambda: FMT20.PerfectInformation(
                merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
            ),
        )

    def test_set_invalid_merger_policy(self):
        self.setupModel()
        self.assertRaises(
            FMT20.Exceptions.MergerPolicyNotAvailable,
            lambda: FMT20.PerfectInformation.merger_policy.fset(
                self.model, FMT20.MergerPolicies.Intermediate_late_takeover_prohibited
            ),
        )

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel()
        self.assertFalse(self.model.is_laissez_faire_optimal())


class TestStrictPerfectInformation(TestPerfectInformation):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel()
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(startup_assets=0.01)
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            startup_assets=0.06,
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            development_costs=0.075,
            success_probability=0.79,
            private_benefit=0.07,
            incumbent_profit_without_innovation=0.3,
            startup_profit_duopoly=0.11,
            incumbent_profit_with_innovation=0.4,
        )
        self.assertEqual(FMT20.MergerPolicies.Strict, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestIntermediatePerfectInformation(TestPerfectInformation):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertTrue(self.model.is_late_takeover)

    def test_not_profitable_not_credit_rationed_unsuccessful(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
            development_success=False,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            development_costs=0.09,
            incumbent_profit_without_innovation=0.35,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
            consumer_surplus_duopoly=0.46,
            consumer_surplus_without_innovation=0.2,
            consumer_surplus_with_innovation=0.35,
        )
        self.assertEqual(
            FMT20.MergerPolicies.Intermediate_late_takeover_allowed,
            self.model.merger_policy,
        )
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestLaissezFairePerfectInformation(TestPerfectInformation):
    def test_not_profitable_not_credit_rationed(self):
        self.setupModel(merger_policy=FMT20.MergerPolicies.Laissez_faire)
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_not_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            startup_assets=0.01,
            private_benefit=0.099,
            success_probability=0.51,
            development_costs=0.1,
            startup_profit_duopoly=0.339,
            incumbent_profit_duopoly=0.01,
            incumbent_profit_with_innovation=0.35,
            consumer_surplus_with_innovation=0.4,
            incumbent_profit_without_innovation=0.3,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.No, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertFalse(self.model.is_owner_investing)
        self.assertFalse(self.model.is_development_successful)
        self.assertFalse(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_not_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            development_costs=0.078,
            success_probability=0.76,
            incumbent_profit_with_innovation=0.51,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertFalse(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Pooling, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)

    def test_profitable_credit_rationed(self):
        self.setupModel(
            merger_policy=FMT20.MergerPolicies.Laissez_faire,
            private_benefit=0.075,
            startup_assets=0.005,
            development_costs=0.076,
            success_probability=0.79,
            incumbent_profit_with_innovation=0.179,
            incumbent_profit_without_innovation=0.08,
            incumbent_profit_duopoly=0.05,
            startup_profit_duopoly=0.1,
        )
        self.assertEqual(FMT20.MergerPolicies.Laissez_faire, self.model.merger_policy)
        self.assertTrue(self.model.is_startup_credit_rationed)
        self.assertEqual(FMT20.Takeover.Separating, self.model.early_bidding_type)
        self.assertEqual(FMT20.Takeover.No, self.model.late_bidding_type)
        self.assertTrue(self.model.is_owner_investing)
        self.assertTrue(self.model.is_development_successful)
        self.assertTrue(self.model.is_early_takeover)
        self.assertFalse(self.model.is_late_takeover)


class TestEquityContract(Test.TestOptimalMergerPolicy):
    """
    Tests Fumagalli_Motta_Tarantino_2020.Models.BaseExtended.EquityContract.
    """

    def setupModel(self, **kwargs) -> None:
        self.model = FMT20.EquityContract(**kwargs)

    def test_thresholds(self):
        self.setupModel()
        self.assertEqual(
            self.model.asset_threshold, self.model.asset_threshold_late_takeover
        )

    def test_debt_not_preferred(self):
        self.setupModel()
        self.assertFalse(self.model.does_startup_prefer_debt())

    def test_debt_preferred(self):
        self.setupModel(merger_policy=FMT20.MergerPolicies.Laissez_faire)
        self.assertTrue(self.model.does_startup_prefer_debt())

    def test_intermediate_optimal_merger_policy(self):
        self.setupModel(
            private_benefit=0.09,
            startup_profit_duopoly=0.15,
            incumbent_profit_duopoly=0.16,
            incumbent_profit_without_innovation=0.36,
        )
        self.assertFalse(self.model.is_intermediate_optimal())

    def test_laissez_faire_optimal_merger_policy(self):
        self.setupModel(
            development_costs=3,
            private_benefit=2,
            consumer_surplus_with_innovation=4,
            consumer_surplus_duopoly=6,
            consumer_surplus_without_innovation=2,
            incumbent_profit_duopoly=1,
            incumbent_profit_without_innovation=3,
            incumbent_profit_with_innovation=7,
            startup_profit_duopoly=5,
        )
        self.assertFalse(self.model.is_laissez_faire_optimal())
