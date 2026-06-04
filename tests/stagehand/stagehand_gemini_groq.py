import argparse
import json
import os
from pathlib import Path

MODULE_PLANS = {
    "manufacturing": {
        "name": "Manufacturing",
        "description": "Pruebas de Manufacturing sobre BOM, Work Orders, Production Planning y rutas de producción.",
        "tests": [
            {"id": "MFG-01", "title": "Crear BOM exitosamente", "objective": "Validar la creación y cálculo de costos de una lista de materiales"},
            {"id": "MFG-02", "title": "Validar cantidades en BOM", "objective": "Asegurar que las cantidades no sean 0 y que el BOM tenga al menos un item"},
            {"id": "MFG-03", "title": "Generar Work Order", "objective": "Crear una orden de trabajo a partir de un BOM y validar su estado"},
            {"id": "MFG-04", "title": "Validar actualización de Work Order", "objective": "Actualizar cantidad y estado de una orden de trabajo"},
            {"id": "MFG-05", "title": "Planificación de producción", "objective": "Simular el planificador de producción y validar el uso de estaciones de trabajo"}
        ],
        "example_prompt": "Genera un plan de pruebas E2E para una lista de materiales y órdenes de trabajo en el módulo Manufacturing de ERPNext. Incluye validaciones de cantidad, costos y workflow de producción."
    },
    "quality_management": {
        "name": "Quality Management",
        "description": "Pruebas de Quality Management sobre procedimientos, revisiones, acciones correctivas, metas y reuniones.",
        "tests": [
            {"id": "QM-01", "title": "Crear procedimiento de calidad", "objective": "Validar inicialización y estructura de un procedimiento de calidad"},
            {"id": "QM-02", "title": "Crear revisión de calidad", "objective": "Asegurar que la revisión validada pueda asociarse a un procedimiento y su estado cambie correctamente"},
            {"id": "QM-03", "title": "Registrar acción correctiva", "objective": "Crear una acción de calidad con resolución y verificar el estado"},
            {"id": "QM-04", "title": "Crear meta de calidad", "objective": "Generar un objetivo de calidad con indicadores y actualizar su progreso"},
            {"id": "QM-05", "title": "Flujo completo de calidad", "objective": "Crear procedimiento, revisión, acción y meta dentro de un workflow integrado"}
        ],
        "example_prompt": "Genera casos de prueba para Quality Management en ERPNext que cubran procedimientos, revisiones, acciones correctivas y metas de calidad."
    },
    "shopping_cart": {
        "name": "Shopping Cart",
        "description": "Pruebas de Shopping Cart sobre carrito, orden de venta, pagos, impuestos y descuentos.",
        "tests": [
            {"id": "SC-01", "title": "Crear carrito y orden de venta", "objective": "Agregar items al carrito y validar la creación de una sales order"},
            {"id": "SC-02", "title": "Calcular total del carrito", "objective": "Validar subtotales, descuentos y total final"},
            {"id": "SC-03", "title": "Aplicar descuento", "objective": "Aplicar descuento por porcentaje y validar el precio final"},
            {"id": "SC-04", "title": "Calcular impuestos automáticos", "objective": "Verificar impuestos en la orden de venta según la configuración fiscal"},
            {"id": "SC-05", "title": "Procesar pago exitoso", "objective": "Simular un flujo de pago y validar el estado de la orden"}
        ],
        "example_prompt": "Genera un conjunto de pruebas E2E para el Shopping Cart de ERPNext, incluyendo carrito, descuentos, impuestos y pagos."
    }
}


def get_api_keys(skip_api_check: bool = False):
    google_key = os.environ.get("GOOGLE_GEMINI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")

    if not skip_api_check and (not google_key or not groq_key):
        raise EnvironmentError(
            "Faltan variables de entorno: GOOGLE_GEMINI_API_KEY y/o GROQ_API_KEY. "
            "No guarde las claves en el código fuente."
        )

    return {
        "google_gemini_api_key": google_key,
        "groq_api_key": groq_key,
    }


def generate_stagehand_plan(module: str):
    if module == "all":
        return {
            "modules": MODULE_PLANS,
            "description": "Plan global de stagehand para Manufacturing, Quality Management y Shopping Cart."
        }

    if module not in MODULE_PLANS:
        raise ValueError(f"Módulo desconocido: {module}")

    plan = MODULE_PLANS[module].copy()
    plan["reference_files"] = [
        "tests/e2e/test_manufacturing_e2e.py",
        "tests/e2e/test_quality_management_e2e.py",
        "tests/e2e/test_shopping_cart_e2e.py"
    ]
    plan["integration_notes"] = (
        "Este plan sirve de base para generar prompts de IA con Google Gemini y Groq. "
        "Extiende el script con llamadas HTTP o SDK según los requisitos de tu entorno."
    )
    return plan


def save_plan(plan, output_path: Path, output_format: str):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_format == "json":
        with output_path.open("w", encoding="utf-8") as handle:
            json.dump(plan, handle, indent=2, ensure_ascii=False)
    else:
        lines = [f"# Stagehand Plan: {plan.get('name', 'Global')}\n"]
        if plan.get("description"):
            lines.append(plan["description"] + "\n")
        if plan.get("tests"):
            lines.append("## Casos de prueba\n")
            for test in plan["tests"]:
                lines.append(f"- **{test['id']}**: {test['title']} — {test['objective']}")
            lines.append("")
        if plan.get("example_prompt"):
            lines.append("## Prompt de ejemplo\n")
            lines.append(f"{plan['example_prompt']}\n")
        if plan.get("integration_notes"):
            lines.append("## Notas de integración\n")
            lines.append(plan["integration_notes"] + "\n")
        if plan.get("reference_files"):
            lines.append("## Archivos de referencia\n")
            for ref in plan["reference_files"]:
                lines.append(f"- {ref}")

        with output_path.open("w", encoding="utf-8") as handle:
            handle.write("\n".join(lines))


def parse_args():
    parser = argparse.ArgumentParser(description="Generador de stagehand para pruebas IA con Gemini y Groq.")
    parser.add_argument("--module", choices=["manufacturing", "quality_management", "shopping_cart", "all"], default="all")
    parser.add_argument("--output", default="tests/stagehand/stagehand_plan.json")
    parser.add_argument("--format", choices=["json", "md"], default="json")
    parser.add_argument("--skip-api-check", action="store_true", help="Genera el plan sin validar las variables de entorno.")
    return parser.parse_args()


def main():
    args = parse_args()
    api_keys = get_api_keys(skip_api_check=args.skip_api_check)

    if args.skip_api_check:
        print("Advertencia: las claves no se verifican. Usa este modo sólo para generar planes locales.")

    plan = generate_stagehand_plan(args.module)

    if args.format == "json" and args.module == "all":
        save_plan(plan, Path(args.output), "json")
    else:
        if args.module == "all":
            for module_name in MODULE_PLANS:
                module_plan = generate_stagehand_plan(module_name)
                output_path = Path(args.output).with_name(f"{module_name}_stagehand.{args.format}")
                save_plan(module_plan, output_path, args.format)
                print(f"Guardado: {output_path}")
            return
        save_plan(plan, Path(args.output), args.format)
        print(f"Guardado: {args.output}")

    print("API keys detectadas:", "OK" if api_keys["google_gemini_api_key"] and api_keys["groq_api_key"] else "FALTAN")


if __name__ == "__main__":
    main()
