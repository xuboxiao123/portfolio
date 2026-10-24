let systemCatalog=null,systemResourceError='';
const systemKinds={video:'独立视频',playlist:'课程播放列表',recordings:'录像目录 / 受限录播',slides:'官方讲义 / 幻灯片',notes:'详细课程笔记',code:'官方代码',lab:'Lab / 实作',exercise:'练习 / Tutorial',assignment:'Assignment / Project',homepage:'官方主页',outline:'课程大纲',local:'已接入中文辅导课',search:'待核实线索'};
const systemPurpose={teacher_materials:'授课教师公开主题视频 · 非完整学期录播',official_lecture:'原版讲座',third_party_revision:'第三方短复习 / 考试解析',third_party_preview:'第三方试听 / 预习',third_party_repost:'第三方转载 · 版本待核实'};
const systemAccess={user_screenshot:'用户截图确认有视频 · 链接/全集未复核',public_page:'网页已核实可访问',public_listing:'公开列表已核实',metadata_public:'视频元数据可取',restricted_listing:'目录公开 · 无可访问子资料',http_403:'未登录读取403 · 权限待确认',login_required:'需要登录及课程权限',linked_not_opened:'官方列出 · 子页未核实',fetch_failed:'本次访问失败',local:'本机资料'};

let systemCatalogPromise=null;
const systemResourceLimits={},systemLocalFilters={};
function ensureSystemCatalog(){
 if(systemCatalog||systemCatalogPromise||systemResourceError)return systemCatalogPromise;
 systemCatalogPromise=api('/api/system-courses').then(d=>{systemCatalog=d;if(model&&route()[0]==='courses'&&route()[1]==='systems')render();return d}).catch(e=>{systemResourceError='资源目录未载入：'+e.message;systemCatalogPromise=null;if(model&&route()[1]==='systems')render()});
 return systemCatalogPromise;
}
function systemAvailability(c){return c.studyAvailability||{group:'missing_lecture',lectures:c.recordingReadiness||'整套讲座待核实',practice:'习题待核实'}}
function systemCourseTile(c){
 const a=systemAvailability(c),cpu=c.localSupplement;
 return `<section class="tile system-course-tile"><span class="tag">${esc(c.direction||c.technologies.slice(0,2).join(' · '))}</span><h3>${esc(c.code)} · ${esc(c.name)}</h3><p><strong>讲座：</strong>${esc(a.lectures)}</p><p><strong>练习：</strong>${esc(a.practice)}</p>${c.qualityWarning?`<p class="system-quality-note">${esc(c.qualityWarning)}</p>`:''}${cpu?`<p class="system-cpu-note">已整合CPU：${cpu.videos}个视频${cpu.pdfs?' · '+cpu.pdfs+'份PDF':''}，在本课内观看。</p>`:''}<button class="primary" data-route="courses/systems/${esc(c.id)}">打开讲座与练习</button></section>`;
}
function systemResourcesView(id){
 if(!systemCatalog){ensureSystemCatalog();return `<section class="panel"><h2>UNSW课外自学资源库</h2><p>${esc(systemResourceError||'正在读取课程资源…')}</p></section>`}
 if(id==='career')return systemCareerLearningView();
 const courses=systemCatalog.courses,c=courses.find(x=>x.id===id);
 const header=`<section class="hero"><span class="tag">课外自学 · ${esc(systemCatalog.updatedAt)}</span><h2>我的课外自学课程</h2><p>讲座和练习按能否取得分组；CPU中文辅导与官方资料放在同一门课里。</p><p class="muted">省内存：视频和PDF点开才加载，关闭预览即可释放。已有目录不等于整套完整、已逐条播放。</p><div class="actions"><button data-route="courses/systems">全部课外课程</button><button data-route="courses/systems/career">名校字幕课 · 全栈与AI实践</button><a class="btn" href="/api/system-courses?download=1" download="UNSW课程资源库.json">导出目录</a></div></section>`;
 if(!c){
  const groups=[['ready','讲座和练习都已找到','可以开始学；旧学期、教师主题课、Lab、Notebook或项目框架的差异保留在各课程内。'],['lecture_only','已有讲座，习题还需补齐','可以先看课；完整配套习题或作业尚未取得。'],['missing_lecture','待补资料：尚未取得整套讲座','尚未取得整套录像的课程。']].filter(([group])=>!systemCatalog.displayPolicy?.hideCoursesWithoutLecture||group!=='missing_lecture');
  const visibleIds=new Set(courses.filter(x=>!systemCatalog.displayPolicy?.hideCoursesWithoutLecture||systemAvailability(x).group!=='missing_lecture').map(x=>x.id));const tracks=(systemCatalog.learningTracks||[]).map(t=>({...t,courses:t.courses.filter(id=>visibleIds.has(id))})).filter(t=>t.courses.length);
  return header+groups.map(([group,title,note])=>{const rows=courses.filter(c=>systemAvailability(c).group===group);return `<section class="panel system-availability-heading"><h3>${title} · ${rows.length}门</h3><p>${note}</p></section><div class="grid system-course-grid" data-system-availability="${group}">${rows.map(systemCourseTile).join('')}</div>`}).join('')+`<details class="panel"><summary>按兴趣方向查看 / 课程编号说明</summary>${tracks.map(t=>`<h4>${esc(t.title)}</h4><div class="actions">${t.courses.map(id=>{const x=courses.find(c=>c.id===id);return x?`<button data-route="courses/systems/${esc(id)}">${esc(x.code)}</button>`:''}).join('')}</div>`).join('')}<ul>${(systemCatalog.courseNumberNotes||[]).map(s=>`<li>${esc(s)}</li>`).join('')}</ul></details><details class="panel"><summary>资料核查与选课意向</summary><p>正式选课未更改。</p><p>已核实完整视频：${courses.filter(c=>c.verifiedFullVideo).length}门。此处的“找到”表示有可学习的资料，视频完整性、实际播放和习题覆盖范围仍逐项标记。</p><p>${esc(systemCatalog.recommendationReview?.spreadsheetReview?.scope||'')}</p></details>`;
 }
 const a=systemAvailability(c),own=systemCatalog.resources.filter(r=>r.course===id&&r.kind!=='local');
 return header+`<section class="panel"><h2>${esc(c.code)} · ${esc(c.name)}</h2><p>${esc(c.learningReason)}</p><p><strong>讲座：</strong>${esc(a.lectures)}</p><p><strong>练习：</strong>${esc(a.practice)}</p>${c.recordingAudit?`<aside class="system-recording-audit"><h3>${esc(c.recordingAudit.heading)}</h3><p>${esc(c.recordingAudit.explanation)}</p><p>${esc(c.recordingAudit.examples)}</p><p><strong>尚未核实：</strong>${esc(c.recordingAudit.limits)}</p><a href="${esc(safeURL(c.recordingAudit.source))}" target="_blank" rel="noopener">查看时长与版本依据</a></aside>`:''}<details><summary>版本、完整性与学习路线</summary><p>${esc(c.summary)}</p><p>${esc(c.recordingReadiness||'')}</p>${c.sourceClarification?`<p><strong>来源说明：</strong>${esc(c.sourceClarification)}</p>`:''}<h3>本课建议学习路线</h3><ol>${(c.learningPath||[]).map(s=>`<li>${esc(s)}</li>`).join('')}</ol>${c.historicalAudit?`<p>已查学期：${esc(c.historicalAudit.termsChecked.join('、'))}</p>`:''}</details><a class="btn" href="${esc(safeURL(c.homepage))}" target="_blank" rel="noopener">官方主页</a></section><section id="system-resource-preview" class="panel local-material-viewer" hidden></section>${c.localSupplement?systemLocalCoursePanel(c):''}${Object.entries(systemKinds).filter(([k])=>k!=='local').map(([kind,title])=>{const rows=own.filter(r=>r.kind===kind);return rows.length?`<details class="panel system-resource-group" ${['playlist','recordings'].includes(kind)?'open':''}><summary><strong>${esc(title)} · ${rows.length}</strong></summary><div id="system-group-${esc(kind)}">${systemResourceGroupRows(id,kind)}</div></details>`:''}).join('')}`;
}
function systemCareerLearningView(){
 const d=systemCatalog.careerLearning;if(!d)return '<section class="panel"><p>学习路线尚未载入，请刷新页面。</p></section>';
 const links=rows=>rows.map(x=>`<p><a href="${esc(safeURL(x.url))}" target="_blank" rel="noopener">${esc(x.title)}</a><br><span class="muted">${esc(x.note)}</span></p>`).join('');
 return `<section class="hero"><span class="tag">${esc(d.checkedAt)} · 名校课程 / 中文讲解 / 项目实践</span><h2>${esc(d.title)}</h2><p>${esc(d.intro)}</p><button data-route="courses/systems">返回UNSW资源库</button></section><section class="panel"><h3>先学什么：全栈与AI开发</h3><ol>${d.skillOrder.map(s=>`<li>${esc(s)}</li>`).join('')}</ol><p>${esc(d.projectPlan)}</p></section><section class="panel"><h3>CPU辅导课：试听与整套课程核对</h3><p>${esc(d.cpu.finding)}</p>${links(d.cpu.links)}<details><summary>比较整套课程时看什么</summary><p>${esc(d.cpu.questions)}</p></details><p>${esc(d.cpu.existing)}</p><button data-route="courses/summer">打开已接入的本地辅导资料</button></section><section class="panel"><h3>WebCMS公开资源仍然保留</h3><p>${esc(d.webcms)}</p><a href="${esc(safeURL(d.webcmsSource))}" target="_blank" rel="noopener">9313官方历史公告</a></section>${d.paths.map((c,i)=>`<section class="panel"><span class="tag">${esc(c.stage)}</span><h3>${i+1}. ${esc(c.name)}</h3><p><strong>资料形式：</strong>${esc(c.format)}</p><p><strong>学习内容：</strong>${esc(c.topics)}</p><p><strong>动手做：</strong>${esc(c.project)}</p><details><summary>课程入口、中文资源与覆盖说明</summary>${links(c.links)}<p>${esc(c.limit)}</p></details></section>`).join('')}<section class="panel"><h3>招聘要求：雇主原始页面样例</h3><p>${esc(d.jobScope)}</p>${d.jobSamples.map(j=>`<article><h4><a href="${esc(safeURL(j.url))}" target="_blank" rel="noopener">${esc(j.name)}</a></h4><p>${esc(j.requirements)}</p></article>`).join('')}</section><details class="panel"><summary>没有当成整套录播的资料与核查说明</summary>${links(d.excluded)}<p>${esc(d.verification)}</p></details>`;
}
function systemResourceGroupRows(course,kind){
 const rows=systemCatalog.resources.filter(r=>r.course===course&&r.kind===kind),limit=systemResourceLimits[course+'/'+kind]||12;
 return rows.slice(0,limit).map(systemResourceRow).join('')+(rows.length>limit?`<button data-system-more="${esc(kind)}" data-system-course="${esc(course)}">再显示12项（共${rows.length}项）</button>`:'');
}
function systemLocalCoursePanel(c){
 if(typeof localCourseIndex==='undefined'||!localCourseIndex){if(typeof ensureLocalCourseIndex==='function')ensureLocalCourseIndex();return `<section class="panel"><h3>CPU中文辅导 · 与本课整合</h3><p>正在读取本机${c.localSupplement.videos}个视频${c.localSupplement.pdfs?'和'+c.localSupplement.pdfs+'份PDF':''}目录…</p></section>`}
 const filter=systemLocalFilters[c.id]||'video',rows=localCourseIndex.files.filter(x=>x.course===c.id),kinds=['video','pdf','code','notebook','image','text','archive','document'].filter(k=>rows.some(x=>x.kind===k));
 return `<section class="panel"><h3>CPU中文辅导 · 与本课整合</h3><p>${esc(c.localSupplement.term)} · ${c.localSupplement.videos}个视频${c.localSupplement.pdfs?' · '+c.localSupplement.pdfs+'份PDF':''}。F盘原件，在本课预览区观看与对照。</p><label>本地资料类型 <select data-system-local-kind="${esc(c.id)}">${kinds.map(k=>`<option value="${k}" ${k===filter?'selected':''}>${esc(localMaterialKinds[k])}</option>`).join('')}</select></label><p class="muted">${esc(c.localSupplement.review)} 视频不自动播放；配套PDF手动选择。</p><div id="system-local-list">${systemLocalRows(c.id,filter)}</div></section>`;
}
function systemLocalRows(course,kind){
 const rows=localCourseIndex.files.filter(x=>x.course===course&&x.kind===kind&&!x.duplicateOf).sort((a,b)=>(a.week??999)-(b.week??999)||a.relative.localeCompare(b.relative,'zh-CN',{numeric:true})),limit=systemResourceLimits['local/'+course+'/'+kind]||12;
 return rows.slice(0,limit).map(x=>`<div class="local-material-row"><div><strong>${esc(x.name)}</strong><p class="muted">${esc(x.relative)} · ${esc(materialSize(x.bytes))}</p></div><button data-system-local="${esc(x.id)}">${kind==='video'?'观看':'打开'}</button></div>`).join('')+(rows.length>limit?`<button data-system-local-more="${esc(course)}">再显示12份</button>`:'');
}
function systemResourceRow(r){
 const source=r.source!==r.url?`<a href="${esc(safeURL(r.source))}" target="_blank" rel="noopener">来源证据</a>`:'';
 return `<article class="system-resource-row"><h4>${esc(r.title)}</h4>${r.purpose?`<p><span class="tag orange">${esc(systemPurpose[r.purpose]||r.purpose)}</span></p>`:''}<p><span class="tag">${esc(r.term)}</span> <span class="tag">${esc(systemCatalog.statusLabels[r.status]||r.status)}</span> <span class="tag">${esc(systemAccess[r.access]||r.access)}</span></p><p>${esc(r.note)}</p><p class="muted">${esc(r.publisher)} · ${esc(r.checkedAt)}${['video','playlist','recordings'].includes(r.kind)?(r.verification.playbackVerified?' · 已实际播放核验':' · 未实际播放核验'):''}</p><div class="actions"><a class="btn" href="${esc(safeURL(r.url))}" target="_blank" rel="noopener">${r.kind==='search'?'打开搜索线索':'原站打开'}</a>${r.kind!=='search'&&!['http_403','login_required','restricted_listing'].includes(r.access)?`<button data-system-preview="${r.id}">在平台内尝试打开</button>`:''}${source}</div></article>`;
}
function closeSystemPreview(){
 const host=$('system-resource-preview');if(!host)return;
 host.querySelectorAll('video,audio').forEach(v=>{v.pause();v.removeAttribute('src');v.load()});host.querySelectorAll('iframe').forEach(f=>f.removeAttribute('src'));host.replaceChildren();host.hidden=true;
}
document.addEventListener('change',e=>{
 const course=e.target.dataset.systemLocalKind;if(!course)return;systemLocalFilters[course]=e.target.value;$('system-local-list').innerHTML=systemLocalRows(course,e.target.value);
});
document.addEventListener('click',e=>{
 const b=e.target.closest('button');if(!b)return;
 if(b.hasAttribute('data-system-close')){closeSystemPreview();return}
 if(b.dataset.systemMore){const key=b.dataset.systemCourse+'/'+b.dataset.systemMore;systemResourceLimits[key]=(systemResourceLimits[key]||12)+12;$('system-group-'+b.dataset.systemMore).innerHTML=systemResourceGroupRows(b.dataset.systemCourse,b.dataset.systemMore);return}
 if(b.dataset.systemLocalMore){const c=b.dataset.systemLocalMore,k=systemLocalFilters[c]||'video',key='local/'+c+'/'+k;systemResourceLimits[key]=(systemResourceLimits[key]||12)+12;$('system-local-list').innerHTML=systemLocalRows(c,k);return}
 if(!b.dataset.systemPreview&&!b.dataset.systemLocal)return;
 closeSystemPreview();const host=$('system-resource-preview');if(!host)return;
 if(b.dataset.systemLocal){const file=localCourseIndex?.files.find(x=>x.id===b.dataset.systemLocal);if(!file)return;host.innerHTML=`<div id="local-material-viewer">${localMaterialViewer(file)}</div><button data-system-close>关闭全部预览 · 释放内存</button>`}
 else{const r=systemCatalog.resources.find(r=>r.id===b.dataset.systemPreview);if(!r)return;host.innerHTML=`<div class="actions"><h3>${esc(r.title)}</h3><button data-system-close>关闭预览 · 释放内存</button></div><p class="muted">原站限制嵌入时使用“原站打开”。本页同时只加载一个预览。</p><iframe title="${esc(r.title)}" src="${esc(systemResourcePreviewURL(r))}" allow="fullscreen; picture-in-picture" allowfullscreen referrerpolicy="strict-origin-when-cross-origin"></iframe>`}
 host.hidden=false;host.scrollIntoView({block:'start',behavior:'smooth'});
});
function systemResourcePreviewURL(r){
 const u=new URL(r.url);
 if(u.hostname==='youtu.be')return 'https://www.youtube.com/embed/'+encodeURIComponent(u.pathname.slice(1))+'?autoplay=0';
 if(['www.youtube.com','youtube.com'].includes(u.hostname)&&u.searchParams.get('v'))return 'https://www.youtube.com/embed/'+encodeURIComponent(u.searchParams.get('v'))+'?autoplay=0';
 if(['www.youtube.com','youtube.com'].includes(u.hostname)&&u.searchParams.get('list'))return 'https://www.youtube.com/embed/videoseries?list='+encodeURIComponent(u.searchParams.get('list'))+'&autoplay=0';
 if(['www.bilibili.com','bilibili.com'].includes(u.hostname)){
  const bvid=u.pathname.match(/\/video\/(BV[A-Za-z0-9]+)/)?.[1];
  if(bvid){const page=/^[1-9][0-9]*$/.test(u.searchParams.get('p')||'')?u.searchParams.get('p'):'1';return 'https://player.bilibili.com/player.html?bvid='+encodeURIComponent(bvid)+'&page='+page+'&autoplay=0';}
 }
 return r.url;
}
