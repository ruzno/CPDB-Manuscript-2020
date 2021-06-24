# This function adds the policy options to the argument dataframe

def add_policy_options(dataframe):
    # -----------------------------------------
    # we create boolean columns for each policy option
    # this script is organised according to sectors
    # to navigate this code use the key related to each policy option
    # -----------------------------------------

    # GENERAL

    options_general = ['g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7']
    conditions_general = [
        # Climate strategy = g1
        (dataframe['policy_type_of_policy_instrument'].str.contains(r"Climate\s+strategy", case=False)),

        # GHG reduction target = g2
        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"GHG\s+reduction\s+target|"
            r"Formal\s+&\s+legally\s+binding\s+GHG\s+reduction\s+target|"
            r"Political\s+&\s+non-binding\s+GHG\s+reduction\s+target",
            case=False)),

        # Coordinating body for climate strategy = g3
        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Coordinating\s+body\s+for\s+climate\s+strategy",
            case=False)),

        # No fossil fuel subsidies = g4
        (dataframe['policy_sector_name'].str.contains(r"General")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Removal\s+of\s+fossil\s+fuel\s+subsidies",
            case=False)),

        # Support for low-emission and negative emissions RD&D = g5
        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"RD&D\s+funding|"
            r"Research\s+&\s+Development\s+and\s+Deployment|"
            r"Demonstration\s+project|"
            r"Research\s+programme|"
            r"Technology\s+deployment\s+and\s+diffusion|"
            r"Technology\s+development",
            case=False)),

        # Economy-wide energy efficiency target = g6
        (dataframe['policy_sector_name'].str.contains(r"General")) &
        # TODO: include condition for more than one sector

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Energy\s+efficiency\s+target|"
            r"Formal\s+&\s+legally\s+binding\s+energy\s+efficiency\s+target|"
            r"Political\s+&\s+non-binding\s+energy\s+efficiency\s+target",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Renewable target for primary energy = g7
        (dataframe['policy_sector_name'].str.contains(r"General")) &
        # TODO: include condition for more than one sector

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Renewable\s+energy\s+target|"
            r"Formal\s+&\s+legally\s+binding\s+renewable\s+energy\s+target|"
            r"Political\s+&\s+non-binding\s+renewable\s+energy\s+target",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables"))
    ]
    for i in range(len(options_general)):
        col_name = options_general[i]
        dataframe[col_name] = conditions_general[i]

    # ELECTRICITY AND HEAT

    options_electricity = ['eh1', 'eh2', 'eh3', 'eh4', 'eh5', 'eh6', 'eh7', 'eh8', 'eh9', 'eh10']
    conditions_electricity = [
        # Support for highly efficient power plant stock = eh1
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            # Note that not all sub policy instruments are logical, e.g. Buildings codes
            # The real condition is 'codes and standards'
            # If the coder tags any sub policy instrument 'codes and standards' will also be selected
            r"Codes\s+and\s+standards|"
            r"Building\s+codes\s+and\s+standards|"
            r"Industrial\s+air\s+pollution\s+standards|"
            r"Product\s+standards|"
            r"Sectoral\s+standards|"
            r"Vehicle\s+air\s+pollution\s+standards|"
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Energy reduction obligation schemes = eh2
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Obligation\s+schemes",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Renewable energy target for electricity sector = eh3
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Renewable\s+energy\s+target|"
            r"Formal\s+&\s+legally\s+binding\s+renewable\s+energy\s+target|"
            r"Political\s+&\s+non-binding\s+renewable\s+energy\s+target",
            case=False)),
        # TODO: add condition on 'policy type' to be consistent with the general sector

        # Support scheme for renewables = eh4
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Green\s+certificates|"
            r"Obligation\s+schemes|"
            r"Net\s+metering|"
            r"Direct\s+investment|"
            r"Funds\s+to\s+sub-national\s+governments|"
            r"Infrastructure\s+investments|"
            r"Procurement\s+rules|"
            r"RD&D\s+funding|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Grid infrastructure development and electricity storage = eh5
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure\s+investments|"
            r"Grid\s+access\s+and\s+priority\s+for\s+renewables",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Coal and oil phase-out policies = eh6
        # (policies_development['policy_sector_name'].str.contains(r"Electricity\s+and\s+heat")) &
        # The condition above is unnecessary in this code. It is only relevant when subsector is presented in another field
        ((dataframe['policy_sector_name'].str.contains(r"Coal")) |  # Needs to satisfy at least one sub
         (dataframe['policy_sector_name'].str.contains(r"oil"))) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Strategic\s+planning",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Support scheme for CCS = eh7
        # (policies_development['policy_sector_name'].str.contains(r"Electricity\s+and\s+heat")) &
        # The condition above is unnecessary in this code. It is only relevant when subsector is presented in another field
        (dataframe['policy_sector_name'].str.contains(r"CCS")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Demonstration\s+project|"
            r"Infrastructure\s+investments|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Support for non-renewable low-carbon alternatives = eh8
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Direct\s+investment|"
            r"Funds\s+to\s+sub-national\s+governments|"
            r"Infrastructure\s+investments|"
            r"Procurement\s+rules|"
            r"RD&D\s+funding|"
            r"Sectoral\s+standards|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Overarching carbon pricing scheme = eh9
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"GHG\s+emissions\s+allowances|"
            r"GHG\s+emission\s+reduction\s+crediting\s+and\s+offsetting\s+mechanism|"
            r"CO2\s+taxes",
            case=False)),

        # Energy and other taxes = eh10
        (dataframe['policy_sector_name'].str.contains(
            r"Electricity\s+and\s+heat|"
            r"CCS|"
            r"Coal|"
            r"Gas|"
            r"Nuclear|"
            r"Oil|"
            r"Renewables")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Energy\s+and\s+other\s+taxes",
            case=False))

    ]
    for i in range(len(options_electricity)):
        col_name = options_electricity[i]
        dataframe[col_name] = conditions_electricity[i]

    # INDUSTRY

    options_industry = ['i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10', 'i11', 'i12', 'i13', 'i14']
    conditions_industry = [
        # Strategy for material efficiency = i1
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Other\s+mandatory\s+requirements|"

            # Note that not all sub policy instruments are logical, e.g. Buildings codes
            # The real condition is 'codes and standards'
            # If the coder tags any sub policy instrument 'codes and standards' will also be selected
            r"Codes\s+and\s+standards|"
            r"Building\s+codes\s+and\s+standards|"
            r"Industrial\s+air\s+pollution\s+standards|"
            r"Product\s+standards|"
            r"Sectoral\s+standards|"
            r"Vehicle\s+air\s+pollution\s+standards|"
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards",
            case=False)) &

        (dataframe['policy_type'].str.contains(
            r"Energy\s+service\s+demand\s+reduction\s+and\s+resource\s+efficiency")),

        # Support for energy efficiency in industrial production = i2
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Obligation\s+schemes|"
            r"White\s+certificates|"
            r"Voluntary\s+approaches|"
            r"Negotiated\s+agreements|"
            r"Public\s+voluntary\s+schemes|"
            r"Unilateral\s+commitments|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Energy reporting and audits = i3
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Auditing|"
            r"Monitoring",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Performance and equipment standards = i4
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            # Note that not all sub policy instruments are logical, e.g. Buildings codes
            # The real condition is 'codes and standards'
            # If the coder tags any sub policy instrument 'codes and standards' will also be selected
            r"Codes\s+and\s+standards|"
            r"Building\s+codes\s+and\s+standards|"
            r"Industrial\s+air\s+pollution\s+standards|"
            r"Product\s+standards|"
            r"Sectoral\s+standards|"
            r"Vehicle\s+air\s+pollution\s+standards|"
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Support scheme for renewables = i5
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Green\s+certificates|"
            r"Obligation\s+schemes|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Support scheme for CCS = i6
        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Industrial\s+process\s+CO2")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure\s+investments|"
            r"Demonstration\s+project|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Support scheme for fuel switch = i7
        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Industrial\s+energy\s+related")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure\s+investments|"
            r"Demonstration\s+project|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Carbon dioxide removal technology development = i8
        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Negative\s+emissions")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure\s+investments|"
            r"Demonstration\s+project|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Incentives to reduce CH4 from fuel exploration and production = i9

        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Fossil\s+fuel\s+exploration\s+and\s+production")) &

        (dataframe['policy_type'].str.contains(r"Non-energy")),

        # Incentives to reduce landfill CH4 = i10

        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Waste\s+CH4")) &

        (dataframe['policy_type'].str.contains(r"Non-energy")),

        # Incentives to reduce N2O from industrial processes = i11

        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Industrial\s+N2O")) &

        (dataframe['policy_type'].str.contains(r"Non-energy")),

        # Incentives to reduce F-gases = i12

        # (policies_development['policy_sector_name'].str.contains(r"Industry")) &
        # condition above unnecessary when sector and subsector are presented in the same column
        (dataframe['policy_sector_name'].str.contains(r"Fluorinated\s+gases")) &

        (dataframe['policy_type'].str.contains(r"Non-energy")),

        # Overarching carbon pricing scheme = i13
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"GHG\s+emissions\s+allowances|"
            r"GHG\s+emission\s+reduction\s+crediting\s+and\s+offsetting\s+mechanism|"
            r"CO2\s+taxes",
            case=False)),

        # Energy and other taxes = i14
        (dataframe['policy_sector_name'].str.contains(
            r"Industry|"
            r"Fluorinated\s+gases|"
            r"Fossil\s+fuel\s+exploration\s+and\s+production|"
            r"Industrial\s+energy\s+related|"
            r"Industrial\s+N2O|"
            r"Industrial\s+process\s+CO2|"
            r"Negative\s+emissions|"
            r"Waste\s+CH4")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Energy\s+and\s+other\s+taxes",
            case=False))

    ]
    for i in range(len(options_industry)):
        col_name = options_industry[i]
        dataframe[col_name] = conditions_industry[i]

    # BUILDINGS

    options_buildings = ['b1', 'b2', 'b3', 'b4', 'b5', 'b6']
    conditions_buildings = [
        # Urban planning strategies = b1
        (dataframe['policy_sector_name'].str.contains(
            r"Buildings|"
            r"Appliances|"
            r"Construction|"
            r"Heating\s+and\s+cooling|"
            r"Hot\s+water\s+and\s+cooking")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure/s+investments|"
            r"Strategic\s+planning",
            case=False)) &

        (dataframe['policy_type'].str.contains(
            r"Energy\s+service\s+demand\s+reduction\s+and\s+resource\s+efficiency")),

        # Building codes and standards as well as support for highly efficient construction = b2
        (dataframe['policy_sector_name'].str.contains(r"Construction")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            # Note that not all sub policy instruments are logical, e.g. Buildings codes
            # The real condition is 'codes and standards'
            # If the coder tags any sub policy instrument 'codes and standards' will also be selected
            r"Codes\s+and\s+standards|"
            r"Building\s+codes\s+and\s+standards|"
            r"Industrial\s+air\s+pollution\s+standards|"
            r"Product\s+standards|"
            r"Sectoral\s+standards|"
            r"Vehicle\s+air\s+pollution\s+standards|"
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Performance and equipment standards as well as support for highly efficient appliances = b3
        (dataframe['policy_sector_name'].str.contains(r"Appliances")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Product\s+standards|"
            r"Performance\s+label|"
            r"Comparison\s+label|"
            r"Endorsement\s+label|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Support scheme for heating and cooling = b4
        (dataframe['policy_sector_name'].str.contains(r"Heating\s+and\s+cooling")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Obligation schemes|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Support scheme for hot water and cooking = b5
        (dataframe['policy_sector_name'].str.contains(r"Hot\s+water\s+and\s+cooking")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Obligation\s+schemes|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Energy and other taxes = b6
        (dataframe['policy_sector_name'].str.contains(
            r"Buildings|"
            r"Appliances|"
            r"Construction|"
            r"Heating\s+and\s+cooling|"
            r"Hot\s+water\s+and\s+cooking")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Energy\s+and\s+other\s+taxes",
            case=False))

    ]
    for i in range(len(options_buildings)):
        col_name = options_buildings[i]
        dataframe[col_name] = conditions_buildings[i]

    # LAND TRANSPORT

    options_transport = ['lt1', 'lt2', 'lt3', 'lt4', 'lt5', 'lt6', 'lt7']
    conditions_transport = [
        # Urban planning and infrastructure investment = lt1
        (dataframe['policy_sector_name'].str.contains(
            r"Transport|"
            r"Air|"
            r"Heavy-duty\s+vehicles|"
            r"Light-duty\s+vehicles|"
            r"Low-emissions\s+mobility|"
            r"Rail|"
            r"Shipping")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure/s+investments|"
            r"Strategic\s+planning",
            case=False)) &

        (dataframe['policy_type'].str.contains(
            r"Energy\s+service\s+demand\s+reduction\s+and\s+resource\s+efficiency")),

        # Energy/emissions performance standards or support for energy efficient light-duty vehicles = lt2
        (dataframe['policy_sector_name'].str.contains(r"Light-duty\s+vehicles")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Energy/emissions performance standards or support for energy efficient heavy-duty vehicles = lt3
        (dataframe['policy_sector_name'].str.contains(r"Heavy-duty\s+vehicles")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Energy\s+efficiency")),

        # Support scheme for biofuels = lt4
        (dataframe['policy_sector_name'].str.contains(
            r"Transport|"
            r"Air|"
            r"Heavy-duty\s+vehicles|"
            r"Light-duty\s+vehicles|"
            r"Low-emissions\s+mobility|"
            r"Rail|"
            r"Shipping")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Obligation schemes|"

            r"Renewable energy target|"
            r"Formal & legally binding renewable energy target|"
            r"Political & non-binding renewable energy target|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Renewables")),

        # Support for modal share switch = lt5
        (dataframe['policy_sector_name'].str.contains(
            r"Transport|"
            r"Air|"
            r"Heavy-duty\s+vehicles|"
            r"Light-duty\s+vehicles|"
            r"Low-emissions\s+mobility|"
            r"Rail|"
            r"Shipping")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Infrastructure/s+investments|"
            r"Strategic\s+planning",
            case=False)) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Support for low-emissions land transportation = lt6
        (dataframe['policy_sector_name'].str.contains(r"Low-emissions\s+mobility")) &

        (dataframe['policy_type'].str.contains(r"Other\s+low-carbon\s+technologies\s+and\s+fuel\s+switch")),

        # Tax on fuel and/or emissions = lt7
        (dataframe['policy_sector_name'].str.contains(
            r"Transport|"
            r"Air|"
            r"Heavy-duty\s+vehicles|"
            r"Light-duty\s+vehicles|"
            r"Low-emissions\s+mobility|"
            r"Rail|"
            r"Shipping")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes",
            case=False))

    ]
    for i in range(len(options_transport)):
        col_name = options_transport[i]
        dataframe[col_name] = conditions_transport[i]

    # AGRICULTURE AND FORESTRY

    options_agriculture = ['af1', 'af2', 'af3', 'af4', 'af5', 'af6']
    conditions_agriculture = [
        # Standards and support for sustainable agricultural practices and use of agricultural products = af1
        (dataframe['policy_sector_name'].str.contains(
            r"Agriculture\s+and\s+forestry")) &

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Product\s+standards|"
            r"Strategic\s+planning|"

            # Note that not all sub policy instruments are logical, e.g. User charges
            # The real condition is 'Fiscal or financial incentives'
            # If the coder tags any sub policy instrument 'Fiscal or financial incentives' will also be selected

            r"Fiscal\s+or\s+financial\s+incentives|"
            r"CO2\s+taxes|"
            r"Energy\s+and\s+other\s+taxes|"
            r"Feed-in\s+tariffs\s+or\s+premiums|"
            r"Grants\s+and\s+subsidies|"
            r"Loans|"
            r"Retirement\s+premium|"
            r"Tax\s+relief|"
            r"Tendering\s+schemes|"
            r"User\s+charges",
            case=False)),

        # Incentives to reduce CO2 emissions from agriculture = af2
        (dataframe['policy_sector_name'].str.contains(r"Agricultural\s+CO2")),

        # Incentives to reduce CH4 emissions from agriculture = af3
        (dataframe['policy_sector_name'].str.contains(r"Agricultural\s+CH4")),

        # Incentives to reduce N2O emissions from agriculture = af3
        (dataframe['policy_sector_name'].str.contains(r"Agricultural\s+N2O")),

        # Incentives to reduce deforestation and enhance afforestation and reforestation = af5
        (dataframe['policy_sector_name'].str.contains(r"Forestry")),

        # Sustainability standards for biomass use = af6

        (dataframe['policy_type_of_policy_instrument'].str.contains(
            r"Product\s+standards")) &

        (dataframe['policy_type'].str.contains(
            r"Renewables"))

    ]

    for i in range(len(options_agriculture)):
        col_name = options_agriculture[i]
        dataframe[col_name] = conditions_agriculture[i]

    options_columns = options_general + options_industry + options_buildings + options_transport + options_agriculture + \
                      options_electricity

    return dataframe


# This function adds fuzziness to the argument dataframe

def add_f(dataframe):
    # calculates sector FUZZINESS - F
    # each policy can cover one of multiple sectors
    # the more fuzzy the policy, the more multi-sectoral the policy approach is

    import numpy as np

    list_sectors = ['GeneralSector', 'ElectricitySector',
                    'IndustrySector', 'BuildingsSector', 'TransportSector', 'LandSector']

    dataframe['F'] = 0

    for col in list_sectors:
        dataframe['F'] = np.where(dataframe['GeneralSector'], 5, dataframe['F'] + dataframe[col] * 1)

    return dataframe


# This function adds sector specificity to the argument dataframe

def add_sp(dataframe):
    # calculates sector SPECIFICITY - Sp
    # each policy can cover the sector as a whole or be cover a sub-sector, which indicates it is more specific
    # 1 = only sector level
    # 2 = sector + sub-sector levels

    dataframe['Sp'] = (dataframe['policy_sector_name'].str.contains(
        r"Agricultural CH4|"
        r"Agricultural CO2|"
        r"Agricultural N2O|"
        r"Forestry|"
        r"Appliances|"
        r"Construction|"
        r"Heating and cooling|"
        r"Hot water and cooking|"
        r"CCS|"
        r"Coal|"
        r"Gas|"
        r"Nuclear|"
        r"Oil|"
        r"Renewables|"
        r"Fluorinated gases|"
        r"Fossil fuel exploration and production|"
        r"Industrial energy related|"
        r"Industrial N2O|"
        r"Industrial process CO2|"
        r"Negative emissions|"
        r"Waste CH4|"
        r"Air|"
        r"Heavy-duty vehicles|"
        r"Light-duty vehicles|"
        r"Low-emissions mobility|"
        r"Rail|"
        r"Shipping", case=False)) * 1 + 1
    return dataframe


# This function adds the policy instrument types to the argument dataframe

def add_pi(dataframe):
    dataframe['DirectInvestment'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Direct\s+investment|"
        r"Funds\s+to\s+sub-national\s+governments|"
        r"Infrastructure\s+investments|"
        r"Procurement\s+rules|"
        r"RD&D\s+funding", case=False)

    dataframe['FiscalFinancialIncentives'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Fiscal\s+or\s+financial\s+incentives|"
        r"Economic\s+Instruments|"
        r"CO2\s+taxes|"
        r"Energy\s+and\s+other\s+taxes|"
        r"Feed-in\s+tariffs\s+or\s+premiums|"
        r"Grants\s+and\s+subsidies|"
        r"Loans|"
        r"Tax\s+relief|"
        r"User\s+changes|"
        r"Tendering\s+schemes|"
        r"Retirement\s+premium|"
        r"User\s+charges", case=False)

    dataframe['Market-basedInstruments'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Market-based\s+instruments|"
        r"GHG\s+emissions\s+allowances|"
        r"GHG\s+emission\s+reduction\s+crediting\s+and\s+offsetting\s+mechanism|"
        r"Green\s+certificates|"
        r"White\s+certificates", case=False)

    dataframe['CodesStandards'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Codes\s+and\s+standards|"
        r"Building\s+codes\s+and\s+standards|"
        r"Product\s+Standards|"
        r"Sectoral\s+Standards|"
        r"Industrial\s+air\s+pollution\s+standards|"
        r"Vehicle\s+fuel-economy\s+and\s+emissions\s+standards|"
        r"Vehicle\s+air\s+pollution\s+standards", case=False)

    dataframe['OtherRegulatoryInstruments'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Regulatory Instruments|"
        r"Auditing|"
        r"Monitoring|"
        r"Obligation\s+schemes|"
        r"Other\s+mandatory\s+requirements", case=False)

    dataframe['RDD'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Research\s+&\s+Development\s+and\s+Deployment|"
        r"Research\s+programme|"
        r"Technology\s+deployment\s+and\s+diffusion|"
        r"Technology\s+development|"
        r"Demonstration\s+project", case=False)

    dataframe['InformationEducation'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Information\s+and+\s+education|"
        r"Performance\s+label|"
        r"Comparison\s+label|"
        r"Endorsement\s+label|"
        r"Advice\s+or\s+aid\s+in\s+implementation|"
        r"Information\s+provision|"
        r"Professional\s+training\s+and\s+qualification", case=False)

    dataframe['PolicySupport'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Policy\s+support|"
        r"Institutional\s+creation|"
        r"Strategic\s+planning", case=False)

    dataframe['VoluntaryApproaches'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Voluntary\s+Approaches|"
        r"Negotiated\s+agreements|"
        r"Public\s+voluntary\s+schemes|"
        r"Unilateral\s+commitments", case=False)

    dataframe['BarrierRemoval'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Barrier\s+removal|"
        r"Net\s+metering|"
        r"Removal\s+of\s+fossil\s+fuel\s+subsidies|"
        r"Removal\s+of\s+split\s+incentives|"
        r"Grid\s+access\s+and\s+priority\s+for\s+renewables", case=False)

    dataframe['ClimateStrategy'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Formal\s+&\s+legally\s+binding\s+climate\s+strategy|"
        r"Political\s+&\s+non-binding\s+climate\s+strategy|"
        r"Coordinating\s+body\s+for\s+climate\s+strategy|"
        r"Climate\s+strategy", case=False)

    dataframe['Target'] = dataframe['policy_type_of_policy_instrument'].str.contains(
        r"Target|"
        r"Energy\s+efficiency\s+target|"
        r"GHG\s+reduction\s+target|"
        r"Renewable\s+energy\s+target", case=False)
    return dataframe


# This function adds the sectors to the argument dataframe

def add_sec(dataframe):
    dataframe['GeneralSector'] = dataframe['policy_sector_name'].str.contains(
        "General")

    dataframe['ElectricitySector'] = dataframe['policy_sector_name'].str.contains(
        r"Electricity\s+and\s+heat|"
        r"Nuclear|"
        r"Coal|"
        r"CCS|"
        r"Gas|"
        r"Oil|"
        r"Renewables", case=False)

    dataframe['IndustrySector'] = dataframe['policy_sector_name'].str.contains(
        r"Industry|"
        r"Negative\s+emissions|"
        r"Industrial\s+process\s+CO2|"
        r"Industrial\s+energy\s+related|"
        r"Fossil\s+fuel\s+exploration\s+and\s+production|"
        r"Industrial\s+N2O|"
        r"Fluorinated\s+gases|"
        r"Waste\s+CH4", case=False)

    dataframe['BuildingsSector'] = dataframe['policy_sector_name'].str.contains(
        r"Buildings|"
        r"Construction|"
        r"Appliances|"
        r"Hot\s+water\s+and\s+cooking|"
        r"Heating\s+and\s+cooling", case=False)

    dataframe['TransportSector'] = dataframe['policy_sector_name'].str.contains(
        r"Transport|"
        r"Low-emissions\s+mobility|"
        r"Public\s+transport|"
        r"Light\s+duty\s+vehicles|"
        r"Shipping|"
        r"Heavy\s+duty\s+vehicles|"
        r"Air|"
        r"Rail", case=False)

    dataframe['LandSector'] = dataframe['policy_sector_name'].str.contains(
        r"Forestry|"
        r"Agriculture\s+and\s+forestry|"
        r"Agricultural\s+CH4|"
        r"Agricultural\s+N2O|"
        r"Agricultural\s+CO2")
    return dataframe
