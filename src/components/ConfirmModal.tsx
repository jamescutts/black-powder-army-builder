"use client";

import type { ReactNode } from "react";
import { Button, Group, Modal, Text } from "@mantine/core";

interface Props {
  opened: boolean;
  title: string;
  children: ReactNode;
  confirmLabel: string;
  onConfirm: () => void;
  onCancel: () => void;
}

/** A small yes/no dialog for actions that throw work away, such as clearing or switching an army. */
export function ConfirmModal({ opened, title, children, confirmLabel, onConfirm, onCancel }: Props) {
  return (
    <Modal
      opened={opened}
      onClose={onCancel}
      title={title}
      centered
      size="sm"
      styles={{ title: { fontFamily: "var(--font-heading), Georgia, serif", fontWeight: 600, fontSize: "1.15rem" } }}
    >
      <Text size="sm" mb="lg">
        {children}
      </Text>
      <Group justify="flex-end" gap="xs">
        <Button variant="default" onClick={onCancel} data-autofocus>
          Keep my army
        </Button>
        <Button color="red" onClick={onConfirm}>
          {confirmLabel}
        </Button>
      </Group>
    </Modal>
  );
}
