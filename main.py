import streamlit as st
import bittensor as bt
import pandas as pd

def display_meta():
    # Initialize metagraph with your specific netid
    netid = 27  # Replace with your actual netid
    metagraph = bt.metagraph(netid, lite=True)
    miner_version_summary = {}
    validator_version_summary = {}

    # Prepare data for display
    data = []

    for hotkey in metagraph.hotkeys:
        index = metagraph.hotkeys.index(hotkey)
        axon = metagraph.axons[index]
        stake = metagraph.stake[index]
        trust = metagraph.trust[index]
        v_trust = metagraph.validator_trust[index]
        v_permit = metagraph.validator_permit[index]
        active = metagraph.active[index]
        if v_trust == 0:
            data.append([index, hotkey, active, stake, trust, v_permit, v_trust, axon.ip, axon.port, axon.version])
            if axon.version in miner_version_summary:
                miner_version_summary[axon.version] += 1
            else:
                miner_version_summary[axon.version] = 1
        else:
            val_version = metagraph.neurons[index].prometheus_info.version
            data.append([index, hotkey, active, stake, trust, v_permit, v_trust, axon.ip, axon.port, val_version])
            if val_version in validator_version_summary:
                validator_version_summary[val_version] += 1
            else:
                validator_version_summary[val_version] = 1

    # Convert to DataFrame for display
    columns = ['UID', 'Hotkey', 'Active', 'Stake', 'Trust', 'V_Permit', 'V_Trust', 'IP', 'Port', 'Version']
    df = pd.DataFrame(data, columns=columns)

    # Streamlit UI
    st.title('Subnet 27 Metagraph Data Summary')
    st.write('### Metagraph Nodes Data')
    st.dataframe(df)

    # Validator version summary
    validator_count = sum(validator_version_summary.values())
    validator_summary_data = [
        {'Version': version, 'Count': count, 'Percentage': f"{count / validator_count * 100:.2f}%"}
        for version, count in validator_version_summary.items()
    ]
    validator_summary_df = pd.DataFrame(validator_summary_data)

    st.write('### Validator Version Summary')
    st.write(f'Total Validator Count: {validator_count}')
    st.dataframe(validator_summary_df)

    # Miner version summary
    miner_count = sum(miner_version_summary.values())
    miner_summary_data = [
        {'Version': version, 'Count': count, 'Percentage': f"{count / miner_count * 100:.2f}%"}
        for version, count in miner_version_summary.items()
    ]
    miner_summary_df = pd.DataFrame(miner_summary_data)

    st.write('### Miner Version Summary')
    st.write(f'Total Miner Count: {miner_count}')
    st.dataframe(miner_summary_df)


if __name__ == '__main__':
    display_meta()


