"use client";

import { getDayjsTz } from "@common/day-js-extended";
import type { CalendarState, EventSlotRenderFragment } from "@schema";
import type React from "react";
import CalendarAddEventPopover from "@/components/dashboard/calendars/calendar-add-event-popover";
import { useI18n } from "@/components/providers/dictionary-provider";
import { useDynamicContext } from "@/hooks/use-dynamic-context";

type FragmentCellProps = {
	fragment: EventSlotRenderFragment;
	fallbackCount: number;
	showTitle: boolean;
};

function FragmentCell({
	fragment,
	fallbackCount,
	showTitle,
}: FragmentCellProps) {
	const { state, setState } = useDynamicContext<CalendarState>();
	const { format } = useI18n();

	const colCount = fragment.columnCount ?? fallbackCount;
	const colWidth = 90 / colCount;
	const colIndex = fragment.columnIndex ?? 0;
	const leftPercent = colIndex * colWidth;

	const dayjsTz = getDayjsTz(state.defaultCalendar.timezone);
	const start = dayjsTz(fragment.event.startsAt);
	const end = dayjsTz(fragment.event.endsAt);
	const popoverKey = fragment.event?.instanceId ?? fragment.event.id;

	const openEventEditor = () => {
		setState((prev) => ({
			...prev,
			activePopoverEditEvent: fragment.event,
			activePopoverId: popoverKey,
		}));
	};
	const handleEventClick: React.MouseEventHandler<HTMLButtonElement> = (
		event,
	) => {
		event.stopPropagation();
		openEventEditor();
	};

	return (
		<CalendarAddEventPopover
			opened={state.activePopoverId === popoverKey}
			onChange={() => {
				setState((prev) => ({
					...prev,
					activePopoverId: null,
					activePopoverEditEvent: undefined,
				}));
			}}
			start={start}
			end={end}
		>
			<button
				type="button"
				className="absolute border-0 bg-brand/80 px-1 text-left text-white rounded-sm shadow-xl text-[10px] leading-tight overflow-hidden cursor-pointer pointer-events-auto"
				style={{
					top: `${fragment.topPercent}%`,
					height: `${fragment.heightPercent}%`,
					left: `${leftPercent}%`,
					width: `${colWidth}%`,
				}}
				onClick={handleEventClick}
			>
				{showTitle && (
					<div
						className={"flex flex-wrap"}
						title={`${fragment.event.title} - ${format.time(start.toDate(), { timeZone: state.defaultCalendar.timezone })} - ${format.time(end.toDate(), { timeZone: state.defaultCalendar.timezone })}`}
					>
						<div className="truncate font-medium text-xs">
							{fragment.event.title}
						</div>
						<div className="truncate font-medium text-xs mx-1">
							{format.time(start.toDate(), {
								timeZone: state.defaultCalendar.timezone,
							})}{" "}
							-{" "}
							{format.time(end.toDate(), {
								timeZone: state.defaultCalendar.timezone,
							})}
						</div>
					</div>
				)}
			</button>
		</CalendarAddEventPopover>
	);
}

function CalendarEventsLayer({
	fragments,
}: {
	fragments: EventSlotRenderFragment[];
}) {
	const fallbackCount = fragments.length || 1;

	const titleOwners = new Set<EventSlotRenderFragment>();
	const grouped = new Map<string, EventSlotRenderFragment[]>();

	for (const f of fragments) {
		const key = `${f.event.id}-${f.date}`;
		const arr = grouped.get(key);
		if (arr) arr.push(f);
		else grouped.set(key, [f]);
	}

	for (const arr of grouped.values()) {
		let owner = arr[0];
		for (const f of arr) {
			if (f.topPercent < owner.topPercent) owner = f;
		}
		titleOwners.add(owner);
	}

	return (
		<div className="absolute inset-0 z-50 pointer-events-none">
			{fragments.map((fragment, index) => {
				const popoverKey = fragment.event?.instanceId ?? fragment.event.id;
				return (
					<FragmentCell
						key={`${popoverKey}-${fragment.date}-${
							fragment.topPercent
						}-${fragment.columnIndex ?? 0}-${index}`}
						fragment={fragment}
						fallbackCount={fallbackCount}
						showTitle={titleOwners.has(fragment)}
					/>
				);
			})}
		</div>
	);
}

export default CalendarEventsLayer;
