DEFAULT = {
    # Universal zone parameters
    "zone_margin_vertical": 20E-6,
    "zone_padding_horizontal": 5.5E-6,
    "zone_padding_vertical": 5.5E-6,
    # Readout zone parameters
    "n_rows_readout": 5,
    "sites_per_row_readout": 3,
    "row_spacing_readout": 5.5E-6,
    "site_spacing_readout": 10E-6,#5.5E-6,
    # Entanglement zone parameters
    "n_rows_entanglement": 5,
    "sites_per_row_entanglement": 3,
    "row_spacing_entanglement": 5.5E-6,
    "site_spacing_entanglement": 10E-6,#5.5E-6,
    "rydberg_blockade_radius": 2E-6,
    # Storage zone parameters
    "n_rows_storage": 16,
    "sites_per_row_storage": 3,
    "row_spacing_storage": 5.5E-6,
    "site_spacing_storage": 10E-6,#5.5E-6,
    # Transport parameters
    "transport_offset": 1E-6,
    "max_transport_speed": 300 * 0.725E-6/1E-6,
    "min_transport_speed": 0.25E-6/1E-6,
    # Physical parameters
    "delta_x": 0.05E-6,
    "delta_y": 0.05E-6,
    "epsilon_fill": 0.007,
    "T1_time": 4,
    "T2_time": 2,
    "atom_loss_pre": 0.0025,
    "atom_loss_post": 0.001,
    "measurement_fidelity": 0.9983,
}
