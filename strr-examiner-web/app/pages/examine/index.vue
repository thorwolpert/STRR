<script setup lang="ts">
import { RoutesE } from '~/enums/routes'
import { useExaminerStore } from '~/store/examiner'

const localePath = useLocalePath()
const { getNextApplication } = useExaminerStore()

const nextApp = await getNextApplication()
navigateTo(localePath(`${RoutesE.EXAMINE}/${nextApp}`))

</script>
