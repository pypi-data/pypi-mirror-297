import { useMemo, type MouseEvent, useEffect, useRef } from 'react'
import { PlusIcon, XCircleIcon } from '@heroicons/react/24/solid'
import { EnumSize, EnumVariant } from '~/types/enum'
import { Button } from '../button/Button'
import clsx from 'clsx'
import { type EditorTab, useStoreEditor } from '~/context/editor'
import { useStoreProject } from '@context/project'
import { isFalse, isNil, isNotNil } from '@utils/index'
import { useStoreContext } from '@context/context'
import { ModelDirectory } from '@models/directory'
import { ModelFile } from '@models/file'

export default function EditorTabs(): JSX.Element {
  const modules = useStoreContext(s => s.modules)
  const models = useStoreContext(s => s.models)
  const lastSelectedModel = useStoreContext(s => s.lastSelectedModel)
  const setLastSelectedModel = useStoreContext(s => s.setLastSelectedModel)

  const files = useStoreProject(s => s.files)
  const selectedFile = useStoreProject(s => s.selectedFile)
  const setSelectedFile = useStoreProject(s => s.setSelectedFile)

  const tab = useStoreEditor(s => s.tab)
  const tabs = useStoreEditor(s => s.tabs)
  const replaceTab = useStoreEditor(s => s.replaceTab)
  const createTab = useStoreEditor(s => s.createTab)
  const selectTab = useStoreEditor(s => s.selectTab)
  const addTab = useStoreEditor(s => s.addTab)

  const [tabsLocal, tabsRemote] = useMemo(() => {
    const local: EditorTab[] = []
    const remote: EditorTab[] = []

    tabs.forEach(tab => {
      if (tab.file.isLocal) {
        local.push(tab)
      }

      if (tab.file.isRemote) {
        remote.push(tab)
      }
    })

    return [local, remote]
  }, [tabs])

  useEffect(() => {
    if (
      isNil(selectedFile) ||
      tab?.file === selectedFile ||
      selectedFile instanceof ModelDirectory ||
      isFalse(modules.hasFiles)
    )
      return

    setLastSelectedModel(models.get(selectedFile.path))

    const newTab = createTab(selectedFile)
    const shouldReplaceTab =
      isNotNil(tab) &&
      tab.file instanceof ModelFile &&
      isFalse(tab.file.isChanged) &&
      tab.file.isRemote &&
      isFalse(tabs.has(selectedFile))

    if (shouldReplaceTab) {
      replaceTab(tab, newTab)
    } else {
      addTab(newTab)
    }

    selectTab(newTab)
  }, [selectedFile])

  useEffect(() => {
    if (isNil(lastSelectedModel)) return

    const file = files.get(lastSelectedModel.path)

    if (isNil(file)) return

    setSelectedFile(file)
  }, [lastSelectedModel])

  function addTabAndSelect(): void {
    const tab = createTab()

    addTab(tab)
    selectTab(tab)
    setSelectedFile(tab.file)
  }

  return (
    <div className="flex items-center">
      <Button
        className="h-6 m-0 ml-1 mr-2 border-none"
        variant={EnumVariant.Alternative}
        size={EnumSize.sm}
        onClick={(e: MouseEvent) => {
          e.stopPropagation()

          addTabAndSelect()
        }}
      >
        <PlusIcon className="inline-block w-3 h-4" />
      </Button>
      <ul className="w-full whitespace-nowrap min-h-[2rem] max-h-[2rem] overflow-hidden overflow-x-auto hover:scrollbar scrollbar--horizontal">
        {tabsLocal.map((tab, idx) => (
          <Tab
            key={tab.id}
            tab={tab}
            title={`Custom SQL ${idx + 1}`}
          />
        ))}
        {tabsRemote.map(tab => (
          <Tab
            key={tab.id}
            tab={tab}
            title={tab.file.name}
          />
        ))}
      </ul>
    </div>
  )
}

function Tab({ tab, title }: { tab: EditorTab; title: string }): JSX.Element {
  const elTab = useRef<HTMLLIElement>(null)

  const addConfirmation = useStoreContext(s => s.addConfirmation)

  const setSelectedFile = useStoreProject(s => s.setSelectedFile)

  const activeTab = useStoreEditor(s => s.tab)
  const selectTab = useStoreEditor(s => s.selectTab)
  const closeTab = useStoreEditor(s => s.closeTab)

  useEffect(() => {
    if (isNil(tab)) return

    tab.el = elTab.current ?? undefined

    if (activeTab?.id === tab.id) {
      setTimeout(() => {
        tab?.el?.scrollIntoView({
          behavior: 'smooth',
          inline: 'center',
        })
      }, 300)
    }
  }, [elTab, tab, activeTab])

  function closeEditorTabWithConfirmation(): void {
    if (tab.file.isChanged) {
      addConfirmation({
        headline: 'Closing Tab',
        description:
          'All unsaved changes will be lost. Do you want to close the tab anyway?',
        yesText: 'Yes, Close Tab',
        noText: 'No, Cancel',
        action: () => {
          closeTab(tab.file)
        },
      })
    } else {
      closeTab(tab.file)
    }
  }

  const isActive = tab.file.id === activeTab?.file.id

  return (
    <li
      ref={elTab}
      className={clsx(
        'inline-block py-1 pr-2 last-child:pr-0 overflow-hidden text-center overflow-ellipsis cursor-pointer',
      )}
      onClick={(e: MouseEvent) => {
        e.stopPropagation()

        selectTab(tab)
        setSelectedFile(tab.file)
      }}
    >
      <span
        className={clsx(
          'flex border-2 justify-between items-center pl-1 pr-1 py-[0.125rem] min-w-[8rem] rounded-md group border-transparent border-r border-r-theme-darker dark:border-r-theme-lighter',
          isActive
            ? 'bg-neutral-200 border-neutral-200 text-neutral-900 dark:bg-dark-lighter dark:border-dark-lighter dark:text-primary-500'
            : 'bg-trasparent hover:bg-theme-darker dark:hover:bg-theme-lighter',
        )}
      >
        <small className="text-xs">{title}</small>
        <small
          className={clsx(
            'group-hover:hidden text-xs inline-block ml-3 mr-1 w-2 h-2 rounded-full',
            tab.file.isChanged ? 'bg-warning-500' : 'bg-transparent',
          )}
        ></small>
        <XCircleIcon
          className="hidden group-hover:inline-block text-neutral-600 dark:text-neutral-100 w-4 h-4 ml-2 mr-0 cursor-pointer"
          onClick={(e: MouseEvent) => {
            e.stopPropagation()

            closeEditorTabWithConfirmation()
          }}
        />
      </span>
    </li>
  )
}
