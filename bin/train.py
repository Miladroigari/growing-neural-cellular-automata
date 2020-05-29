import torch.optim as optim
from torch.nn import MSELoss

from lib.model.callback.plot_metrics import PlotMetrics
from lib.model.callback.plot_output import PlotOutput
from lib.model.callback.save_weights import SaveWeights
from lib.model.cell_growth.cell_growth_model_builder import build_model_from
from lib.model.cell_growth.data_tensor import DataTensor
from lib.script_utils import load_config, init_logger, get_target

if __name__ == "__main__":
    model_name = 'lizard-16x16'

    cfg = load_config(model_name)
    init_logger(cfg)

    model = build_model_from(cfg)
    model.load(cfg['model.weights.path'])

    target = get_target(cfg, model_name)
    initial = DataTensor.initial(target)

    optimizer = optim.Adam(
        model.parameters(),
        lr=cfg['model.train.lr']
    )
    scheduler = optim.lr_scheduler.StepLR(
        optimizer=optimizer,
        step_size=cfg['model.train.scheduler.step_size'],
        gamma=cfg['model.train.scheduler.gamma']
    )

    model.train(
        epochs=cfg['model.train.epochs'],
        steps=(cfg['model.train.steps.min'], cfg['model.train.steps.max']),
        initial=initial,
        target=target,
        optimizer=optimizer,
        scheduler=scheduler,
        loss_fn=MSELoss(reduction='sum'),
        callbacks=[
            PlotMetrics(reset_every=cfg['model.train.metrics.reset_every']),
            PlotOutput(
                every=cfg['model.preview.every'],
                window_size=(cfg['model.preview.width'] * 2, cfg['model.preview.height']),
                target=target
            ),
            SaveWeights(
                path=cfg['model.weights.path'],
                every=cfg['model.weights.save_every']
            )
        ]
    )
