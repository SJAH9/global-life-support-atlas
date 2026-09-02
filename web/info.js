(() => {
  const button=document.querySelector('#theme-toggle');
  if(button)button.addEventListener('click',()=>{const theme=document.documentElement.dataset.theme==='dark'?'light':'dark';document.documentElement.dataset.theme=theme;localStorage.setItem('life-support-theme',theme)});
  const data=window.LIFE_SUPPORT_DATA,gate=document.querySelector('[data-launch-gate]');if(!data||!gate)return;
  const project=data.project,launched=project.participation_enabled&&project.launch_date&&new Date(project.launch_date)<=new Date();
  document.querySelectorAll('[data-project-status]').forEach(item=>item.textContent=launched?'Participation open':'Private development');
  document.querySelector('[data-participation-title]').textContent=launched?'Add a source-bearing observation.':'Not open yet.';
  gate.innerHTML=launched?`<h2>Public intake open</h2><p>Contributions enter review and do not alter a score until provenance, unit, geography, date, and normalization are accepted.</p><a href="${project.repository}/issues/new">Open a contribution record</a>`:`<h2>Launch gate closed</h2><p>${project.launch_date?`Participation is scheduled no earlier than ${project.launch_date}.`:'No launch date has been configured.'} The repository and review queue remain private while source and scoring contracts are tested.</p>`;
})();
