#!/usr/bin/env python3
"""
NeuroString – NeuroPilot (automatický pilot sítě)
"""

import time
import random
import threading
from datetime import datetime
from node import NeuroNode


class NeuroPilot:
    """Automatický pilot pro NeuroString síť.

    NeuroPilot samostatně řídí síť: odesílá transakce, přidává nové uzly
    a zobrazuje průběžný stav – vše bez zásahu uživatele.
    """

    def __init__(self, network, interval=2.0, max_nodes=10):
        """Inicializace NeuroPilotu.

        Args:
            network: instance NeuroNetwork, kterou NeuroPilot spravuje
            interval: prodleva mezi akcemi v sekundách (výchozí 2 s)
            max_nodes: maximální počet uzlů, které NeuroPilot přidá (výchozí 10)
        """
        if interval <= 0:
            raise ValueError("interval musí být kladné číslo")
        if max_nodes < 1:
            raise ValueError("max_nodes musí být alespoň 1")

        self.network = network
        self.interval = interval
        self.max_nodes = max_nodes
        self.running = False
        self._thread = None
        self.actions_performed = 0
        self.started_at = None

    # ------------------------------------------------------------------
    # Veřejné metody
    # ------------------------------------------------------------------

    def start(self):
        """Spustí automatický pilot v samostatném vlákně."""
        if self.running:
            print("⚠️  NeuroPilot již běží.")
            return

        self.running = True
        self.started_at = datetime.now()
        self._thread = threading.Thread(target=self._run, daemon=True)
        self._thread.start()
        print(
            f"🤖 NeuroPilot spuštěn "
            f"(interval: {self.interval} s, max uzlů: {self.max_nodes})"
        )

    def stop(self):
        """Zastaví automatický pilot."""
        if not self.running:
            print("⚠️  NeuroPilot není spuštěn.")
            return

        self.running = False
        if self._thread:
            self._thread.join(timeout=self.interval + 1)
        print(
            f"🛑 NeuroPilot zastaven | "
            f"Provedeno akcí: {self.actions_performed}"
        )

    def get_status(self):
        """Vrátí slovník se stavem NeuroPilotu."""
        elapsed = (
            (datetime.now() - self.started_at).total_seconds()
            if self.started_at
            else 0.0
        )
        return {
            "running": self.running,
            "actions": self.actions_performed,
            "elapsed_seconds": round(elapsed, 1),
            "interval": self.interval,
            "max_nodes": self.max_nodes,
        }

    # ------------------------------------------------------------------
    # Interní logika
    # ------------------------------------------------------------------

    def _run(self):
        """Hlavní smyčka automatického pilota."""
        while self.running:
            self._step()
            time.sleep(self.interval)

    def _step(self):
        """Provede jeden krok automatického pilota."""
        # Transakce jsou 3× pravděpodobnější než přidání uzlu
        action = random.choices(
            ["transaction", "add_node"],
            weights=[3, 1],
            k=1,
        )[0]

        if action == "transaction":
            data = f"autopilot_{datetime.now().timestamp()}"
            result = self.network.process_transaction(data)
            print(f"🤖 [NeuroPilot] Transakce: {result}")

        elif action == "add_node" and len(self.network.nodes) < self.max_nodes:
            node = NeuroNode()
            self.network.add_node(node)
            self.network.activate_quantum_entanglement()
            print(f"🤖 [NeuroPilot] Přidán uzel: {node.node_id}")

        self.actions_performed += 1
