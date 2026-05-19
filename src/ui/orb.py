from __future__ import annotations


PARTICLE_COUNT = 14


def neural_orb(class_prefix: str = "w40") -> str:
    """Return reusable CSS-only neural orb markup with deterministic particles."""
    particles = "\n".join(
        (
            f'<span class="{class_prefix}-orb-particle '
            f'{class_prefix}-orb-particle-{index}"></span>'
        )
        for index in range(1, PARTICLE_COUNT + 1)
    )
    return f"""
<div class="{class_prefix}-orb-shell" aria-hidden="true">
  <div class="{class_prefix}-orb-halo"></div>
  <div class="{class_prefix}-orb-ring {class_prefix}-orb-ring-1"></div>
  <div class="{class_prefix}-orb-ring {class_prefix}-orb-ring-2"></div>
  <div class="{class_prefix}-orb-ring {class_prefix}-orb-ring-3"></div>
  <div class="{class_prefix}-orb-ring {class_prefix}-orb-ring-4"></div>
  <div class="{class_prefix}-orb">
    <div class="{class_prefix}-orb-surface"></div>
    <div class="{class_prefix}-orb-grid"></div>
    <div class="{class_prefix}-orb-core"></div>
    <div class="{class_prefix}-orb-scan"></div>
  </div>
  <div class="{class_prefix}-orb-particles">
    {particles}
  </div>
</div>
""".strip()
